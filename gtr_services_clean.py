import requests
import json
import hashlib
from datetime import datetime

class GTRPayService:
    def __init__(self, mch_id=None, secret_key=None):
        # Load real GTR Pay configuration
        try:
            from gtr_config import GTR_CONFIG
            self.mch_id = mch_id or GTR_CONFIG.get('MERCHANT_ID', '28903878')
            self.secret_key = secret_key or GTR_CONFIG.get('SECRET_KEY', 'fe827fc9afa0409da8fa4be501df3e0f')
            self.passage_id = GTR_CONFIG.get('PASSAGE_ID', 26501)
            self.base_url = GTR_CONFIG.get('BASE_URL', 'https://wg.gtrpay001.com')
            self.enabled = GTR_CONFIG.get('ENABLED', True)
        except ImportError:
            print("⚠️ GTR Config not found - using defaults")
            self.mch_id = mch_id or "28903878"
            self.secret_key = secret_key or "fe827fc9afa0409da8fa4be501df3e0f"
            self.passage_id = 26501
            self.base_url = 'https://wg.gtrpay001.com'
            self.enabled = True
        
    def build_sign_digest(self, data, secret_key):
        """Build signature digest for GTR Pay API"""
        # Sort parameters and create query string
        sorted_params = sorted(data.items())
        query_string = '&'.join([f'{k}={v}' for k, v in sorted_params])
        
        # Add secret key and hash
        sign_string = query_string + '&key=' + secret_key
        sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()
        
        return sign
        
    def create_deposit_payment(self, amount=None, reference=None, callback_url=None, return_url=None, **kwargs):
        """Create deposit payment with real GTR Pay API"""
        try:
            if not self.enabled:
                return {
                    'success': False,
                    'message': 'GTR Pay is not enabled'
                }
            
            # Prepare request data for GTR Pay API
            request_data = {
                "mchId": str(self.mch_id),
                "passageId": str(self.passage_id),
                "orderAmount": str(int(float(amount))),  # Amount in Naira
                "orderNo": str(reference),
                "notifyUrl": str(callback_url or ''),
                "returnUrl": str(return_url or ''),
                "remark": f'Deposit {reference}',
                "goodsName": "Account Deposit",
                "timestamp": str(int(datetime.now().timestamp())),
                "version": "1.0"
            }
            
            # Generate signature
            sign = self.build_sign_digest(request_data, self.secret_key)
            request_data['sign'] = sign
            
            # Make API request to GTR Pay
            api_url = f"{self.base_url}/collect/create"
            
            print(f"🔄 GTR Pay API Request: {api_url}")
            print(f"📊 Request Data: {request_data}")
            
            response = requests.post(
                api_url, 
                json=request_data, 
                headers={'Content-Type': 'application/json'},
                timeout=30,
                verify=False  # SSL verification disabled like PHP
            )
            
            print(f"📥 GTR Pay Response Status: {response.status_code}")
            print(f"📄 GTR Pay Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                
                # GTR Pay returns code as string "200" for success
                if str(result.get('code')) == '200':
                    data = result.get('data', {})
                    return {
                        'success': True,
                        'payment_url': data.get('payUrl'),
                        'trade_no': data.get('tradeNo', reference),
                        'reference': reference,
                        'message': 'Payment created successfully'
                    }
                else:
                    return {
                        'success': False,
                        'message': result.get('msg', 'Failed to create payment')
                    }
            else:
                return {
                    'success': False,
                    'message': f'API request failed with status {response.status_code}'
                }
                
        except Exception as e:
            print(f"❌ GTR Pay Error: {str(e)}")
            return {
                'success': False,
                'message': f'Error creating payment: {str(e)}'
            }
