from gtr_bank_services import gtr_pay_service

print("=== Testing GTR Pay API with Real Implementation ===")
result = gtr_pay_service.create_deposit_payment(100, 'TEST123', 'https://example.com')
print(f"Success: {result['success']}")
print(f"Message: {result.get('message')}")
print(f"Full result: {result}")

print("\n=== Testing with 1000 naira ===")
result2 = gtr_pay_service.create_deposit_payment(1000, 'TEST456', 'https://example.com')
print(f"Success: {result2['success']}")
print(f"Message: {result2.get('message')}")
