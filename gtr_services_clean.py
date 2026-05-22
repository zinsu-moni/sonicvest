import hashlib
from datetime import datetime

import requests


class GTRPayService:
    def __init__(self, mch_id=None, secret_key=None):
        try:
            from gtr_config import GTR_CONFIG

            self.mch_id = mch_id or GTR_CONFIG.get('MERCHANT_ID', '999300111')
            self.secret_key = secret_key or GTR_CONFIG.get('SECRET_KEY', 'e8a4cdd0ccdb4d2b9ca6212453c5e40c')
            self.pay_type = GTR_CONFIG.get('PAY_TYPE', '520')
            self.bank_code = GTR_CONFIG.get('BANK_CODE', 'NGR044')
            self.base_url = GTR_CONFIG.get('BASE_URL', 'https://api.nekpayment.com/pay/web')
            self.enabled = GTR_CONFIG.get('ENABLED', True)
        except ImportError:
            print('⚠️ GTR Config not found - using defaults')
            self.mch_id = mch_id or '999300111'
            self.secret_key = secret_key or 'e8a4cdd0ccdb4d2b9ca6212453c5e40c'
            self.pay_type = '520'
            self.bank_code = 'NGR044'
            self.base_url = 'https://api.nekpayment.com/pay/web'
            self.enabled = True

    def build_sign_digest(self, data, secret_key):
        """Build the documented MD5 signature string."""
        filtered_items = []
        for key, value in data.items():
            if key in {'sign', 'sign_type'}:
                continue
            if value is None:
                continue
            if isinstance(value, str) and value == '':
                continue
            filtered_items.append((key, str(value)))

        sign_string = '&'.join(f'{key}={value}' for key, value in sorted(filtered_items))
        sign_string = f'{sign_string}&key={secret_key}' if sign_string else f'key={secret_key}'
        return hashlib.md5(sign_string.encode('utf-8')).hexdigest()

    def create_deposit_payment(
        self,
        amount=None,
        reference=None,
        callback_url=None,
        page_url=None,
        return_url=None,
        mch_return_msg=None,
        goods_name='Account Deposit',
        pay_type=None,
        bank_code=None,
        **kwargs,
    ):
        """Create a deposit payment using the NekPayment collection API."""
        try:
            if not self.enabled:
                return {
                    'success': False,
                    'message': 'GTR Pay is not enabled',
                }

            amount_value = float(amount)
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            resolved_page_url = page_url or return_url
            resolved_pay_type = str(pay_type or self.pay_type)
            resolved_bank_code = str(bank_code or self.bank_code)

            request_data = {
                'version': '1.0',
                'mch_id': str(self.mch_id),
                'notify_url': str(callback_url or ''),
                'page_url': str(resolved_page_url or ''),
                'mch_order_no': str(reference),
                'pay_type': resolved_pay_type,
                'trade_amount': f'{amount_value:.2f}',
                'order_date': order_date,
                'bank_code': resolved_bank_code,
                'goods_name': str(goods_name),
                'sign_type': 'MD5',
            }

            if mch_return_msg:
                request_data['mch_return_msg'] = str(mch_return_msg)

            request_data['sign'] = self.build_sign_digest(request_data, self.secret_key)

            print(f'🔄 GTR Pay API Request: {self.base_url}')
            print(f'📊 Request Data: {request_data}')

            response = requests.post(
                self.base_url,
                data=request_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=30,
            )

            print(f'📥 GTR Pay Response Status: {response.status_code}')
            print(f'📄 GTR Pay Response: {response.text}')

            if response.status_code != 200:
                return {
                    'success': False,
                    'message': f'API request failed with status {response.status_code}',
                }

            try:
                result = response.json()
            except Exception:
                return {
                    'success': False,
                    'message': f'Invalid JSON response: {response.text}',
                }

            resp_code = str(result.get('respCode') or result.get('code') or '')
            if resp_code != 'SUCCESS':
                return {
                    'success': False,
                    'message': result.get('tradeMsg') or result.get('msg') or 'Failed to create payment',
                }

            payment_url = result.get('payInfo')
            if not payment_url and isinstance(result.get('data'), dict):
                payment_url = result['data'].get('payInfo') or result['data'].get('payUrl')

            if not payment_url:
                return {
                    'success': False,
                    'message': 'Payment URL missing from provider response',
                }

            return {
                'success': True,
                'payment_url': payment_url,
                'trade_no': result.get('orderNo') or result.get('tradeNo') or reference,
                'reference': reference,
                'message': result.get('tradeMsg') or 'Payment created successfully',
            }
        except Exception as e:
            print(f'❌ GTR Pay Error: {str(e)}')
            return {
                'success': False,
                'message': f'Error creating payment: {str(e)}',
            }

    def verify_payment_callback(self, callback_data):
        """Verify the asynchronous collection callback signature."""
        try:
            received_sign = callback_data.get('sign')
            if not received_sign:
                return {'success': False, 'message': 'No signature in callback'}

            signature_payload = {
                'amount': callback_data.get('amount'),
                'mchId': callback_data.get('mchId'),
                'mchOrderNo': callback_data.get('mchOrderNo'),
                'orderDate': callback_data.get('orderDate'),
                'orderNo': callback_data.get('orderNo'),
                'oriAmount': callback_data.get('oriAmount'),
                'tradeResult': callback_data.get('tradeResult'),
            }

            mer_ret_msg = callback_data.get('merRetMsg')
            if mer_ret_msg not in (None, ''):
                signature_payload['merRetMsg'] = mer_ret_msg

            expected_sign = self.build_sign_digest(signature_payload, self.secret_key)
            if received_sign.lower() != expected_sign.lower():
                return {'success': False, 'message': 'Invalid signature'}

            if str(callback_data.get('tradeResult')) != '1':
                return {
                    'success': False,
                    'message': f"Payment not successful: {callback_data.get('tradeResult')}",
                }

            return {
                'success': True,
                'reference': callback_data.get('mchOrderNo'),
                'trade_no': callback_data.get('orderNo'),
                'amount': callback_data.get('amount') or callback_data.get('oriAmount'),
                'status': 'completed',
                'merchant_id': callback_data.get('mchId'),
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error verifying callback: {str(e)}',
            }
