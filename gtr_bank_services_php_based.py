"""
GTR Pay Payment Gateway Integration
Based on the working PHP GTRBankDepositServices implementation
"""

import requests
import json
import hashlib
from datetime import datetime
from flask import url_for

class GTRPayService:
    def __init__(self, mch_id=None, secret_key=None):
        # GTR Pay API Configuration
        self.base_url = "https://wg.gtrpay001.com"
        
        # Try to load from config file
        try:
            from gtr_config import GTR_CONFIG
            self.mch_id = mch_id or GTR_CONFIG.get('MERCHANT_ID', '****')
            self.secret_key = secret_key or GTR_CONFIG.get('SECRET_KEY', 'your_secret_key')
            self.passage_id = GTR_CONFIG.get('PASSAGE_ID', 26501)
            self.enabled = GTR_CONFIG.get('ENABLED', True)
        except ImportError:
            # Fallback if config file doesn't exist
            self.mch_id = mch_id or "****"
            self.secret_key = secret_key or "your_secret_key"
            self.passage_id = 26501
            self.enabled = False  # Disabled if no config
            print("⚠️ GTR Pay config not found. Please create gtr_config.py from gtr_config.example.py")
        
    def create_deposit_payment(self, amount, reference, callback_url=None, return_url=None):
        """
        Create payment with GTR Pay - Based on working PHP implementation
        Amount should be in Naira (e.g., 3000 for ₦3,000)
        """
        try:
            # Check if GTR Pay is enabled
            if not self.enabled:
                return {
                    'success': False,
                    'message': 'GTR Pay is not properly configured. Please contact administrator.'
                }

            if not callback_url:
                # This would be the Flask callback URL for IPN
                callback_url = url_for('gtr_payment_callback', _external=True)

            # Request Body (exactly like PHP implementation)
            request_body = {
                "mchId": str(self.mch_id),
                "passageId": self.passage_id,
                "orderAmount": str(amount),
                "orderNo": str(reference),
                "notifyUrl": str(callback_url),
                "remark": f'Order {reference}',
            }

            # Build Sign (exactly like PHP)
            sign = self.build_sign_digest(request_body.copy(), self.secret_key)
            request_body['sign'] = sign

            print(f"🔄 GTR Pay Request: {request_body}")

            # Send CURL Request (exactly like PHP)
            response = requests.post(
                f"{self.base_url}/collect/create",
                json=request_body,
                headers={'Content-Type': 'application/json'},
                timeout=30,
                verify=False  # SSL verification disabled like PHP
            )

            print(f"📡 GTR Pay Response Status: {response.status_code}")
            print(f"📊 GTR Pay Response: {response.text}")

            # Check HTTP status (like PHP)
            if response.status_code != 200:
                return {
                    'success': False,
                    'message': f'HTTP Error: {response.status_code}'
                }

            # Parse JSON response
            try:
                response_data = response.json()
                print(f"📋 Parsed Response: {response_data}")
            except json.JSONDecodeError:
                return {
                    'success': False,
                    'message': f'Invalid JSON response: {response.text}'
                }

            # Check if successful (handle both string and integer codes)
            code = response_data.get('code')
            if str(code) != '200':
                error_msg = response_data.get('msg', 'Unknown error from GTR Pay')
                print(f"❌ GTR Pay Error: {error_msg}")
                return {
                    'success': False,
                    'message': error_msg
                }

            # Success - extract payment data (like PHP)
            data = response_data.get('data', {})
            if 'payUrl' not in data or 'tradeNo' not in data:
                print(f"⚠️ Missing payment data in response: {data}")
                return {
                    'success': False,
                    'message': 'Invalid response structure from GTR Pay'
                }

            print(f"✅ Payment created successfully!")
            print(f"💳 Payment URL: {data['payUrl']}")
            print(f"🔢 Trade No: {data['tradeNo']}")

            return {
                'success': True,
                'payment_url': data['payUrl'],
                'trade_no': data['tradeNo'],
                'reference': reference,
                'message': 'Payment created successfully'
            }
            
        except Exception as e:
            print(f"💥 Exception in create_deposit_payment: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error creating payment: {str(e)}'
            }
    
    def build_sign_digest(self, data, secret_key):
        """
        Build signature digest - EXACT copy of PHP implementation
        """
        # Remove the 'sign' field from the data (like PHP unset)
        if 'sign' in data:
            del data['sign']
        
        # Sort the array by key in ascending order according to ASCII values (like PHP ksort)
        sorted_data = dict(sorted(data.items()))
        
        # Concatenate the string in the format key=value&key=value
        sign_string = ''
        for key, value in sorted_data.items():
            if value:  # Only include non-empty values (like PHP !empty())
                sign_string += f'{key}={value}&'
        
        # Append the private key to the string
        sign_string += f'key={secret_key}'
        
        print(f"🔐 Sign String: {sign_string}")
        
        # Perform MD5 signature on the generated string (like PHP md5())
        sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
        
        print(f"🔑 Generated Sign: {sign}")
        
        return sign
    
    def verify_payment_callback(self, callback_data):
        """
        Verify payment callback from GTR Pay
        """
        try:
            # Verify signature
            received_sign = callback_data.get('sign')
            if not received_sign:
                return {'success': False, 'message': 'No signature in callback'}
            
            # Build expected signature
            expected_sign = self.build_sign_digest(callback_data.copy(), self.secret_key)
            
            if received_sign != expected_sign:
                return {'success': False, 'message': 'Invalid signature'}
            
            # Check payment status
            status = callback_data.get('status')
            if status == '1':  # Successful payment
                return {
                    'success': True,
                    'reference': callback_data.get('orderNo'),
                    'trade_no': callback_data.get('tradeNo'),
                    'amount': callback_data.get('orderAmount'),
                    'status': 'completed'
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment failed with status: {status}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error verifying callback: {str(e)}'
            }

# Create global instance for import
gtr_pay_service = GTRPayService()
