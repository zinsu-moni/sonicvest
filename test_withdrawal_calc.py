from app import app, db, Withdrawal, User, SYSTEM_SETTINGS

with app.app_context():
    print("=== Withdrawal Fee Check ===")
    print(f"System withdrawal fee percentage: {SYSTEM_SETTINGS['WITHDRAWAL_FEE_PERCENTAGE']}%")
    
    # Check existing withdrawals
    withdrawals = Withdrawal.query.all()
    print(f"Total withdrawal records: {len(withdrawals)}")
    
    for w in withdrawals:
        if w.amount > 0:
            actual_fee_percentage = (w.fee / w.amount) * 100
            print(f"Withdrawal ID {w.id}:")
            print(f"  Amount: ₦{w.amount:,.2f}")
            print(f"  Fee: ₦{w.fee:,.2f}")
            print(f"  Actual Fee %: {actual_fee_percentage:.1f}%")
            
            if actual_fee_percentage > 100:
                print(f"  🚨 PROBLEM: Fee percentage is {actual_fee_percentage:.1f}%!")
            
    # Test calculation with current logic
    test_amount = 3000.0
    expected_fee = test_amount * (SYSTEM_SETTINGS['WITHDRAWAL_FEE_PERCENTAGE'] / 100)
    expected_net = test_amount - expected_fee
    
    print(f"\n=== Test Calculation ===")
    print(f"Test amount: ₦{test_amount:,.2f}")
    print(f"Expected fee (15%): ₦{expected_fee:,.2f}")
    print(f"Expected net: ₦{expected_net:,.2f}")
