"""
Diagnose Package Income Issues
Check which users have packages but haven't received income
"""
from app import app, db, User, UserPackage, Transaction, Package
from datetime import datetime, timedelta

def diagnose_income_issues():
    with app.app_context():
        print("\n" + "="*70)
        print("DIAGNOSING PACKAGE INCOME ISSUES")
        print("="*70)
        
        # Get all user packages
        all_packages = UserPackage.query.order_by(UserPackage.purchase_date.desc()).all()
        
        if not all_packages:
            print("\n❌ No packages found in the database!")
            return
        
        print(f"\n📦 Total packages: {len(all_packages)}")
        
        # Check active packages
        active_packages = [up for up in all_packages if up.is_active and up.end_date > datetime.utcnow()]
        print(f"✅ Active packages: {len(active_packages)}")
        
        # Check packages with no income
        packages_no_income = [up for up in all_packages if (up.total_earned or 0) == 0]
        print(f"⚠️  Packages with zero income: {len(packages_no_income)}")
        
        print("\n" + "-"*70)
        print("PACKAGES WITHOUT INCOME:")
        print("-"*70)
        
        issues_found = []
        
        for up in packages_no_income:
            user = User.query.get(up.user_id)
            package = Package.query.get(up.package_id)
            
            if not user or not package:
                continue
            
            # Calculate expected payouts
            time_since_purchase = datetime.utcnow() - up.start_date
            hours_since_purchase = time_since_purchase.total_seconds() / 3600
            expected_payouts = int(hours_since_purchase / 24)  # Every 24 hours
            
            # Check if package should have received income
            should_have_income = hours_since_purchase >= 24
            
            issue = {
                'user_id': user.id,
                'username': user.username,
                'package_name': package.name,
                'purchase_date': up.start_date,
                'end_date': up.end_date,
                'is_active': up.is_active,
                'last_payout': up.last_payout,
                'daily_return': up.daily_return,
                'total_earned': up.total_earned or 0,
                'hours_since_purchase': hours_since_purchase,
                'expected_payouts': expected_payouts,
                'should_have_income': should_have_income
            }
            
            issues_found.append(issue)
            
            status_emoji = "🔴" if should_have_income else "🟡"
            print(f"\n{status_emoji} User: {user.username} (ID: {user.id})")
            print(f"   Package: {package.name}")
            print(f"   Purchased: {up.start_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Hours since purchase: {hours_since_purchase:.1f}")
            print(f"   Expected payouts: {expected_payouts}")
            print(f"   Daily return: ₦{up.daily_return:,.2f}")
            print(f"   Total earned: ₦{up.total_earned or 0:,.2f}")
            print(f"   Last payout: {up.last_payout or 'Never'}")
            print(f"   Is active: {up.is_active}")
            print(f"   Status: {up.status}")
            
            if should_have_income:
                print(f"   ⚠️  ISSUE: Should have received {expected_payouts} payout(s)")
        
        # Check for transaction records
        print("\n" + "-"*70)
        print("CHECKING INCOME TRANSACTIONS:")
        print("-"*70)
        
        income_transactions = Transaction.query.filter_by(
            type='package_income'
        ).order_by(Transaction.created_at.desc()).limit(10).all()
        
        if income_transactions:
            print(f"\n✅ Found {len(income_transactions)} recent income transactions:")
            for txn in income_transactions:
                user = User.query.get(txn.user_id)
                print(f"   • {user.username}: ₦{txn.amount:,.2f} - {txn.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("\n❌ No income transactions found in database!")
        
        # Check background processor status
        print("\n" + "-"*70)
        print("BACKGROUND PROCESSOR STATUS:")
        print("-"*70)
        print("⚠️  Note: The background income processor runs as a thread")
        print("   when the app starts with 'python app.py'")
        print("   It checks every 30 seconds for packages that need payout")
        print("   Income is distributed every 24 hours after package purchase")
        
        # Summary
        print("\n" + "="*70)
        print("DIAGNOSIS SUMMARY:")
        print("="*70)
        
        critical_issues = [i for i in issues_found if i['should_have_income']]
        
        if critical_issues:
            print(f"\n🔴 CRITICAL: {len(critical_issues)} packages should have received income but haven't")
            print("\nPossible causes:")
            print("   1. Background processor is not running")
            print("   2. App was not started with 'python app.py'")
            print("   3. App was restarted and processor hasn't run yet")
            print("   4. Database connection issues")
            print("\nRecommended actions:")
            print("   1. Check if app is running: ps aux | grep python")
            print("   2. Restart app with: python app.py")
            print("   3. Monitor logs for background processor messages")
            print("   4. Run manual payout script: python manual_income_payout.py")
        else:
            print("\n✅ No critical issues found")
            print("   Packages may be too new to have received income yet")

if __name__ == '__main__':
    diagnose_income_issues()
