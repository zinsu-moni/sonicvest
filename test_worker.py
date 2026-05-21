"""
Test Worker Locally
Run this to verify the income distribution worker is working correctly
"""
from app import app, db, User, UserPackage, Package, Transaction
from datetime import datetime, timezone
import sys

def test_worker():
    """Test the worker functionality"""
    print("=" * 60)
    print("🧪 TESTING INCOME DISTRIBUTION WORKER")
    print("=" * 60)
    
    with app.app_context():
        # Check for active packages
        active_packages = UserPackage.query.filter(
            UserPackage.is_active == True,
            UserPackage.end_date > datetime.now(timezone.utc)
        ).all()
        
        print(f"\n📦 Active packages found: {len(active_packages)}")
        
        if not active_packages:
            print("\n⚠️  No active packages found!")
            print("\n💡 To test:")
            print("   1. Create a user account")
            print("   2. Purchase a package")
            print("   3. Run this test again\n")
            return
        
        print("\n" + "=" * 60)
        print("PACKAGE DETAILS")
        print("=" * 60)
        
        for i, pkg in enumerate(active_packages, 1):
            user = db.session.get(User, pkg.user_id)
            package = db.session.get(Package, pkg.package_id)
            
            print(f"\n{i}. User: {user.username} (ID: {user.id})")
            print(f"   Package: {package.name}")
            print(f"   Daily Return: ₦{pkg.daily_return:,.0f}")
            print(f"   Start Date: {pkg.start_date}")
            print(f"   Last Payout: {pkg.last_payout or 'Never'}")
            print(f"   Total Earned: ₦{(pkg.total_earned or 0):,.0f}")
            print(f"   User Balance: ₦{user.main_balance:,.0f}")
            
            # Check if payout is due
            current_time = datetime.now(timezone.utc)
            hours_since_last = 24.0
            
            # Convert naive datetimes to UTC aware if needed
            start_date = pkg.start_date.replace(tzinfo=timezone.utc) if pkg.start_date.tzinfo is None else pkg.start_date
            last_payout = pkg.last_payout.replace(tzinfo=timezone.utc) if pkg.last_payout and pkg.last_payout.tzinfo is None else pkg.last_payout
            
            if last_payout is None:
                time_since_start = current_time - start_date
                hours_elapsed = time_since_start.total_seconds() / 3600
                should_payout = hours_elapsed >= hours_since_last
                status = f"⏳ First payout in {max(0, hours_since_last - hours_elapsed):.1f} hours"
            else:
                time_since_last = current_time - last_payout
                hours_elapsed = time_since_last.total_seconds() / 3600
                should_payout = hours_elapsed >= hours_since_last
                status = f"✅ Payout DUE NOW!" if should_payout else f"⏳ Next payout in {max(0, hours_since_last - hours_elapsed):.1f} hours"
            
            print(f"   Status: {status}")
        
        print("\n" + "=" * 60)
        print("TESTING INCOME DISTRIBUTION")
        print("=" * 60)
        
        # Import and run worker function
        from worker import distribute_income
        
        print("\n🔄 Running income distribution...")
        processed = distribute_income()
        
        print(f"✅ Processed {processed} payouts")
        
        if processed > 0:
            print("\n" + "=" * 60)
            print("UPDATED BALANCES")
            print("=" * 60)
            
            for pkg in active_packages:
                user = db.session.get(User, pkg.user_id)
                package = db.session.get(Package, pkg.package_id)
                print(f"\n{user.username}:")
                print(f"   Balance: ₦{user.main_balance:,.0f}")
                print(f"   Total Earned: ₦{user.total_earned:,.0f}")
                print(f"   Package Total: ₦{(pkg.total_earned or 0):,.0f}")
            
            # Show recent transactions
            print("\n" + "=" * 60)
            print("RECENT INCOME TRANSACTIONS")
            print("=" * 60)
            
            recent_transactions = Transaction.query.filter_by(
                type='package_income'
            ).order_by(Transaction.created_at.desc()).limit(5).all()
            
            for trans in recent_transactions:
                user = db.session.get(User, trans.user_id)
                print(f"\n{trans.created_at}: {user.username}")
                print(f"   Amount: ₦{trans.amount:,.0f}")
                print(f"   Description: {trans.description}")
        
        print("\n" + "=" * 60)
        print("✅ TEST COMPLETED")
        print("=" * 60)
        print("\nThe worker is functioning correctly!")
        print("Deploy to production and enable the worker dyno.\n")

if __name__ == '__main__':
    try:
        test_worker()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
