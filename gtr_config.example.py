"""
GTR Bank Payment Gateway Integration
Handles deposit processing and verification
"""

import requests
import json
from datetime import datetime

class GTRBankService:
    def __init__(self):
        # GTR Bank API Configuration
        self.base_url = "https://gtrbank.com/gtr_api/api"
        self.api_key = "YOUR_GTR_API_KEY"  # Replace with actual API key
        self.merchant_id = "YOUR_MERCHANT_ID"  # Replace with actual merchant ID
        
    def initiate_payment(self, amount, email, phone, name, reference=None):
        """
        Initiate payment with GTR Bank
        Amount should be in Naira (e.g., 3000 for ₦3,000)
        """
        try:
            # Convert amount to kobo (multiply by 100)
            amount_in_kobo = int(float(amount) * 100)
            
            if not reference:
                reference = f"GTR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{email.split('@')[0]}"
            
            payload = {
                "api_key": self.api_key,
                "merchant_id": self.merchant_id,
                "amount": amount_in_kobo,  # Amount in kobo
                "email": email,
                "phone": phone,
                "name": name,
                "reference": reference,
                "callback_url": "https://yoursite.com/payment/callback",  # Update with your domain
                "return_url": "https://yoursite.com/dashboard"  # Update with your domain
            }
            
            response = requests.post(
                f"{self.base_url}/payment/initialize",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'success': True,
                        'payment_url': data.get('data', {}).get('payment_url'),
                        'reference': reference,
                        'amount': amount,
                        'amount_kobo': amount_in_kobo
                    }
            
            return {
                'success': False,
                'error': f'Payment initialization failed: {response.text}',
                'status_code': response.status_code
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def verify_payment(self, reference):
        """
        Verify payment status with GTR Bank
        """
        try:
            payload = {
                "api_key": self.api_key,
                "merchant_id": self.merchant_id,
                "reference": reference
            }
            
            response = requests.post(
                f"{self.base_url}/payment/verify",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data,
                    'status': data.get('data', {}).get('status'),
                    'amount': data.get('data', {}).get('amount', 0) / 100,  # Convert back to Naira
                    'reference': reference
                }
            
            return {
                'success': False,
                'error': f'Verification failed: {response.text}',
                'status_code': response.status_code
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

# Create global instance
gtr_service = GTRBankService()
