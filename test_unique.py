#!/usr/bin/env python3
"""
Test GTR Pay with unique reference
"""

import secrets
from datetime import datetime

def test_with_unique_ref():
    try:
        from gtr_bank_services import gtr_pay_service
        print("✅ GTR Pay service imported successfully")
        print(f"Merchant ID: {gtr_pay_service.mch_id}")
        print(f"Enabled: {gtr_pay_service.enabled}")
        
        # Generate unique reference
        unique_ref = f"TEST{secrets.token_urlsafe(6).upper()}"
        print(f"\n🔄 Testing payment creation with unique reference: {unique_ref}")
        
        result = gtr_pay_service.create_deposit_payment(
            amount=5000,
            reference=unique_ref,
            callback_url="https://example.com/callback"
        )
        
        print(f"\n📊 Payment Result: {result}")
        
        if result['success']:
            print("✅ Payment creation successful!")
            print(f"Payment URL: {result.get('payment_url')}")
        else:
            print(f"❌ Payment failed: {result['message']}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_unique_ref()
