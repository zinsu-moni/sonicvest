#!/usr/bin/env python3
"""
Test GTR Pay Service independently
"""

if __name__ == "__main__":
    try:
        print("Testing GTR Pay Service...")
        
        # Import and test
        from gtr_bank_services import gtr_pay_service
        print("✅ Import successful")
        
        # Check method signature
        import inspect
        sig = inspect.signature(gtr_pay_service.create_deposit_payment)
        print(f"Method signature: {sig}")
        print(f"Parameters: {list(sig.parameters.keys())}")
        
        # Test method call
        result = gtr_pay_service.create_deposit_payment(
            amount=1000,
            reference="TEST123",
            callback_url="http://example.com/callback",
            return_url="http://example.com/return"
        )
        
        print("✅ Method call successful")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
