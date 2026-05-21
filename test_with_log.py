#!/usr/bin/env python3
"""
Test GTR Pay and save output to file
"""

import sys
from datetime import datetime

def test_and_log():
    log_file = "gtr_test_output.txt"
    
    try:
        with open(log_file, 'w') as f:
            # Redirect stdout to file
            original_stdout = sys.stdout
            sys.stdout = f
            
            print(f"GTR Pay Test - {datetime.now()}")
            print("=" * 50)
            
            from gtr_bank_services import gtr_pay_service
            print("✅ GTR Pay service imported successfully")
            print(f"Merchant ID: {gtr_pay_service.mch_id}")
            print(f"Secret Key: {gtr_pay_service.secret_key[:10]}...")
            print(f"Enabled: {gtr_pay_service.enabled}")
            print(f"Base URL: {gtr_pay_service.base_url}")
            
            print("\n🔄 Testing payment creation...")
            result = gtr_pay_service.create_deposit_payment(
                amount=5000,
                reference="TEST123456",
                callback_url="https://example.com/callback"
            )
            
            print(f"\n📊 Payment Result: {result}")
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            
            # Restore stdout
            sys.stdout = original_stdout
            
        print(f"Test completed. Check {log_file} for results.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_and_log()
