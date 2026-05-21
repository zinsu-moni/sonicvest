from app import app, db, User, UserPackage, Transaction

with app.app_context():
    print("=" * 60)
    print("BACKFILLING TOTAL_EARNED VALUES")
    print("=" * 60)
    
    # Get all user packages with relationships loaded
    all_packages = UserPackage.query.options(
        db.joinedload(UserPackage.package),
        db.joinedload(UserPackage.user)
    ).all()
    
    print(f"\nProcessing {len(all_packages)} packages...")
    updated_count = 0
    
    for user_package in all_packages:
        # Get all completed package income transactions for this user
        # Match by description pattern
        description_pattern = f'Income from {user_package.package.name}'
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_package.user_id,
            Transaction.type == 'package_income',
            Transaction.status == 'completed',
            Transaction.description == description_pattern,
            Transaction.created_at >= user_package.start_date
        ).all()
        
        if transactions:
            # Calculate total earned from transactions
            total_from_transactions = sum(t.amount for t in transactions)
            
            # Update the package's total_earned
            old_value = user_package.total_earned or 0
            user_package.total_earned = total_from_transactions
            
            print(f"\nPackage: {user_package.package.name}")
            print(f"   User: {user_package.user.username}")
            print(f"   Transactions found: {len(transactions)}")
            print(f"   Old total_earned: N{old_value:,.2f}")
            print(f"   New total_earned: N{total_from_transactions:,.2f}")
            
            updated_count += 1
        print(".", end="", flush=True)
    
    # Commit all changes
    try:
        db.session.commit()
        print("\n" + "=" * 60)
        print(f"SUCCESS: Updated {updated_count} packages!")
        print("=" * 60)
    except Exception as e:
        db.session.rollback()
        print(f"\nERROR: Error committing changes: {e}")
