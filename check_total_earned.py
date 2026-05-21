from app import app, db, User, UserPackage, Transaction
from datetime import datetime

with app.app_context():
    print("=" * 60)
    print("CHECKING TOTAL_EARNED VALUES")
    print("=" * 60)
    
    # Get all active user packages
    user_packages = UserPackage.query.filter_by(is_active=True).all()
    
    if not user_packages:
        print("\n❌ No active packages found!")
    else:
        print(f"\n✅ Found {len(user_packages)} active packages:\n")
        
        for up in user_packages:
            user = User.query.get(up.user_id)
            print(f"📦 Package: {up.package.name}")
            print(f"   User: {user.username}")
            print(f"   Amount Invested: ₦{up.amount_invested:,.2f}")
            print(f"   Daily Return: ₦{up.daily_return:,.2f}")
            print(f"   Total Earned (in DB): {up.total_earned}")
            print(f"   Last Payout: {up.last_payout}")
            print(f"   Start Date: {up.start_date}")
            print(f"   End Date: {up.end_date}")
            print(f"   Is Active: {up.is_active}")
            
            # Count package income transactions for this user
            income_count = Transaction.query.filter_by(
                user_id=user.id,
                type='package_income',
                status='completed'
            ).count()
            
            # Sum of package income transactions
            income_sum = db.session.query(db.func.sum(Transaction.amount)).filter_by(
                user_id=user.id,
                type='package_income',
                status='completed'
            ).scalar() or 0
            
            print(f"   Package Income Transactions: {income_count}")
            print(f"   Total from Transactions: ₦{income_sum:,.2f}")
            print(f"   User Main Balance: ₦{user.main_balance:,.2f}")
            print(f"   User Total Earned: ₦{user.total_earned:,.2f}")
            print("-" * 60)
    
    print("\n" + "=" * 60)
    print("CHECKING RECENT PACKAGE INCOME TRANSACTIONS")
    print("=" * 60)
    
    recent_incomes = Transaction.query.filter_by(
        type='package_income',
        status='completed'
    ).order_by(Transaction.created_at.desc()).limit(10).all()
    
    if not recent_incomes:
        print("\n❌ No package income transactions found!")
    else:
        print(f"\n✅ Last {len(recent_incomes)} package income transactions:\n")
        for trans in recent_incomes:
            user = User.query.get(trans.user_id)
            print(f"💰 Amount: ₦{trans.amount:,.2f}")
            print(f"   User: {user.username}")
            print(f"   Description: {trans.description}")
            print(f"   Date: {trans.created_at}")
            print("-" * 60)
