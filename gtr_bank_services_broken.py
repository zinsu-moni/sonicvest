"""
GTR Pay Payment Gateway Integration
Handles deposit processing and verification
Based on the PHP GTRBankDepositServices implementation
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
        Create payment with GTR Pay
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
            
            # Request Body (following PHP format)
            request_body = {
                "mchId": self.mch_id,
                "passageId": self.passage_id,
                "orderAmount": str(amount),
                "orderNo": reference,
                "notifyUrl": callback_url,
                "remark": f'Order {reference}',
            }
            
            # Build signature
            sign = self.build_sign_digest(request_body, self.secret_key)
            request_body['sign'] = sign
            
            # Send request to GTR Pay API
            response = requests.post(
                f"{self.base_url}/collect/create",
                json=request_body,
                headers={'Content-Type': 'application/json'},
                timeout=30,
                verify=False  # SSL verification disabled as in PHP
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '200':
                    return {
                        'success': True,
                        'payment_url': data['data']['payUrl'],
                        'trade_no': data['data']['tradeNo'],
                        'reference': reference
                    }
                else:
                    return {
                        'success': False,
                        'message': data.get('msg', 'Payment creation failed')
                    }
            else:
                return {
                    'success': False,
                    'message': f'HTTP Error: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating payment: {str(e)}'
            }
    
    def build_sign_digest(self, data, secret_key):
        """
        Build signature digest following PHP implementation
        """
        # Remove the 'sign' field from the data
        if 'sign' in data:
            del data['sign']
        
        # Sort the array by key in ascending order according to ASCII values
        sorted_data = dict(sorted(data.items()))
        
        # Concatenate the string in the format key=value&key=value
        sign_string = ''
        for key, value in sorted_data.items():
            if value:  # Only include non-empty values
                sign_string += f'{key}={value}&'
        
        # Append the private key to the string
        sign_string += f'key={secret_key}'
        
        # Perform MD5 signature on the generated string
        sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
        
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
                    'message': 'Payment not successful',
                    'status': 'failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error verifying callback: {str(e)}'
            }

# Create global instance for import
gtr_pay_service = GTRPayService()
