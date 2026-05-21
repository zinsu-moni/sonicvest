#!/usr/bin/env python3

from gtr_bank_services import gtr_pay_service
import secrets

def test_amount(amount):
    ref = f'TEST{secrets.token_urlsafe(4).upper()}'
    print(f'\n=== Testing {amount} naira with reference: {ref} ===')
    
    try:
        result = gtr_pay_service.create_deposit_payment(amount, ref, 'https://example.com/callback')
        print(f'Success: {result["success"]}')
        print(f'Message: {result.get("message", "No message")}')
        
        if result['success']:
            print('✅ Payment URL created successfully!')
            print(f'Payment URL: {result.get("payment_url", "No URL")}')
        else:
            print('❌ Payment creation failed')
            
    except Exception as e:
        print(f'❌ Exception occurred: {e}')

if __name__ == '__main__':
    # Test different amounts
    amounts = [50, 100, 500, 1000, 3000, 5000]
    
    for amount in amounts:
        test_amount(amount)
        
    print('\n=== Summary ===')
    print('Testing complete. Check which amounts work vs fail.')
