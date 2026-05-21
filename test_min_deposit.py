from gtr_bank_services import gtr_pay_service
import secrets

# Test with new minimum amount
ref = f'TEST{secrets.token_urlsafe(4).upper()}'
print(f'Testing GTR Pay with ₦50 deposit (new minimum)')
print(f'Reference: {ref}')

result = gtr_pay_service.create_deposit_payment(50, ref, 'https://example.com/callback')

print(f'\n=== RESULT ===')
print(f'Success: {result["success"]}')
if result['success']:
    print(f'✅ Payment URL created successfully!')
    print(f'Payment URL: {result.get("payment_url", "None")}')
    print(f'Trade No: {result.get("trade_no", "None")}')
else:
    print(f'❌ Error: {result.get("message", "None")}')
