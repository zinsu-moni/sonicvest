from app import app, db, Withdrawal

with app.app_context():
    withdrawals = Withdrawal.query.all()
    print(f"Total withdrawals: {len(withdrawals)}")
    
    for w in withdrawals:
        print(f"ID: {w.id}")
        print(f"Amount: ₦{w.amount:,.2f}")
        print(f"Fee: ₦{w.fee:,.2f}")
        print(f"Net Amount: ₦{w.net_amount:,.2f}")
        print(f"Status: {w.status}")
        print("---")
        
        # Check if fee calculation is correct
        expected_fee = w.amount * (15.0 / 100)
        print(f"Expected fee (15%): ₦{expected_fee:,.2f}")
        if abs(w.fee - expected_fee) > 0.01:
            print(f"⚠️  Fee mismatch! Stored: {w.fee}, Expected: {expected_fee}")
        print("=" * 40)
