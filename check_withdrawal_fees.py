from app import app, db, Withdrawal

with app.app_context():
    withdrawals = Withdrawal.query.all()
    print(f'Total withdrawals: {len(withdrawals)}')
    
    for w in withdrawals:
        print(f'Withdrawal ID: {w.id}')
        print(f'  Amount: ₦{w.amount:,.2f}')
        print(f'  Fee: ₦{w.fee:,.2f}')
        print(f'  Net Amount: ₦{w.net_amount:,.2f}')
        print(f'  Expected fee (15%): ₦{w.amount * 0.15:,.2f}')
        
        # Check if the fee is way too high
        if w.fee > w.amount:
            print(f'  ⚠️  ERROR: Fee is higher than withdrawal amount!')
        
        if w.fee > w.amount * 0.20:  # If fee is more than 20%
            print(f'  ⚠️  WARNING: Fee seems too high - {(w.fee/w.amount)*100:.1f}%')
        
        print('-' * 50)
