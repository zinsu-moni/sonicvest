#!/usr/bin/env python3
"""
Debug GTR Pay Response Issue
"""

def test_gtr_pay_debug():
    try:
        from gtr_bank_services import gtr_pay_service
        print("✅ GTR Pay service imported successfully")
        print(f"Merchant ID: {gtr_pay_service.mch_id}")
        print(f"Enabled: {gtr_pay_service.enabled}")
        
        # Test the payment creation
        print("\n🔄 Testing payment creation...")
        result = gtr_pay_service.create_deposit_payment(
            amount=5000,
            reference="TEST123456",
            callback_url="https://example.com/callback"
        )
        
        print(f"\n📊 Payment Result: {result}")
        
        # Analyze the result
        if result['success']:
            print("✅ Payment creation successful!")
        else:
            print(f"❌ Payment failed: {result['message']}")
            
            # Check for the specific "success" message issue
            if result['message'] == 'success':
                print("🔍 FOUND THE BUG: GTR Pay returned 'success' as error message")
            elif 'success' in result['message']:
                print("🔍 PARTIAL MATCH: Error message contains 'success'")
        
        return result
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_gtr_pay_debug()
