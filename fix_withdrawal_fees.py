from app import app, db, Withdrawal

with app.app_context():
    withdrawals = Withdrawal.query.all()
    print(f'Found {len(withdrawals)} withdrawal records')
    
    fixed_count = 0
    
    for w in withdrawals:
        print(f'Checking Withdrawal ID: {w.id}')
        print(f'  Current: Amount=₦{w.amount:,.2f}, Fee=₦{w.fee:,.2f}')
        
        # Calculate what the fee should be (15%)
        correct_fee = w.amount * 0.15
        correct_net_amount = w.amount - correct_fee
        
        print(f'  Correct: Fee=₦{correct_fee:,.2f}, Net=₦{correct_net_amount:,.2f}')
        
        # Check if fee needs fixing
        if abs(w.fee - correct_fee) > 0.01:  # If difference is more than 1 cent
            print(f'  🔧 Fixing fee from ₦{w.fee:,.2f} to ₦{correct_fee:,.2f}')
            w.fee = correct_fee
            w.net_amount = correct_net_amount
            fixed_count += 1
        else:
            print(f'  ✅ Fee is correct')
        
        print('-' * 50)
    
    if fixed_count > 0:
        db.session.commit()
        print(f'✅ Fixed {fixed_count} withdrawal records')
    else:
        print('✅ All withdrawal records have correct fees')
