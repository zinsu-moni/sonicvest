#!/usr/bin/env python3
"""
Test GTR Pay Service directly
"""

try:
    from gtr_bank_services import gtr_pay_service
    print("✅ Successfully imported gtr_pay_service")
except Exception as e:
    print(f"❌ Error importing gtr_pay_service: {e}")
    exit(1)

def test_payment_creation():
    print("Testing GTR Pay service...")
    print(f"Merchant ID: {gtr_pay_service.mch_id}")
    print(f"Secret Key: {gtr_pay_service.secret_key[:10]}..." if gtr_pay_service.secret_key else "None")
    print(f"Enabled: {gtr_pay_service.enabled}")
    print(f"Base URL: {gtr_pay_service.base_url}")
    
    if not gtr_pay_service.enabled:
        print("❌ GTR Pay service is disabled")
        return
    
    # Test payment creation
    print("\n🔄 Creating test payment...")
    result = gtr_pay_service.create_deposit_payment(
        amount=5000,
        reference="TEST123",
        callback_url="https://example.com/callback"
    )
    
    print(f"\n📊 Payment creation result: {result}")
    return result

if __name__ == "__main__":
    test_payment_creation()
