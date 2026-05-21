from gtr_bank_services import gtr_pay_service
import secrets

# Test with unique reference
ref = f'TEST{secrets.token_urlsafe(4).upper()}'
print(f'Testing GTR Pay with reference: {ref}')

result = gtr_pay_service.create_deposit_payment(5000, ref, 'https://example.com/callback')

print(f'\n=== RESULT ===')
print(f'Success: {result["success"]}')
print(f'Message: {result.get("message", "None")}')
if result['success']:
    print(f'Payment URL: {result.get("payment_url", "None")}')
    print(f'Trade No: {result.get("trade_no", "None")}')
