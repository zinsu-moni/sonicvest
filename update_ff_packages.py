#!/usr/bin/env python3
"""
Update Fintech Finance packages and settings.
This script adds the correct FF packages with proper pricing and returns.
"""

from app import app, db, Package, User
from datetime import datetime

def clear_existing_packages():
    """Remove existing packages"""
    print("🗑️  Removing existing packages...")
    Package.query.delete()
    db.session.commit()
    print("✅ Existing packages cleared")

def create_fintech_packages():
    """Create the official Fintech Finance packages"""
    
    packages = [
        {
            'name': 'FF1',
            'description': 'Entry level package - Perfect for beginners',
            'price': 3000.0,
            'daily_return_rate': 26.17,  # ₦785 / ₦3000 * 100 = 26.17%
            'duration_days': 35
        },
        {
            'name': 'FF2',
            'description': 'Starter package - Steady growth',
            'price': 6000.0,
            'daily_return_rate': 25.83,  # ₦1550 / ₦6000 * 100 = 25.83%
            'duration_days': 35
        },
        {
            'name': 'FF3',
            'description': 'Basic package - Good returns',
            'price': 10000.0,
            'daily_return_rate': 26.50,  # ₦2650 / ₦10000 * 100 = 26.50%
            'duration_days': 35
        },
        {
            'name': 'FF4',
            'description': 'Standard package - Enhanced returns',
            'price': 15000.0,
            'daily_return_rate': 25.33,  # ₦3800 / ₦15000 * 100 = 25.33%
            'duration_days': 35
        },
        {
            'name': 'FF5',
            'description': 'Premium package - High returns',
            'price': 20000.0,
            'daily_return_rate': 28.25,  # ₦5650 / ₦20000 * 100 = 28.25%
            'duration_days': 35
        },
        {
            'name': 'FF6',
            'description': 'Gold package - Excellent returns',
            'price': 25000.0,
            'daily_return_rate': 30.00,  # ₦7500 / ₦25000 * 100 = 30.00%
            'duration_days': 35
        },
        {
            'name': 'FF7',
            'description': 'Platinum package - Superior returns',
            'price': 50000.0,
            'daily_return_rate': 25.10,  # ₦12550 / ₦50000 * 100 = 25.10%
            'duration_days': 35
        },
        {
            'name': 'FF8',
            'description': 'Diamond package - Elite returns',
            'price': 70000.0,
            'daily_return_rate': 21.79,  # ₦15250 / ₦70000 * 100 = 21.79%
            'duration_days': 35
        },
        {
            'name': 'FF9',
            'description': 'Elite package - Premium returns',
            'price': 100000.0,
            'daily_return_rate': 20.50,  # ₦20500 / ₦100000 * 100 = 20.50%
            'duration_days': 35
        },
        {
            'name': 'FF10',
            'description': 'VIP package - Exceptional returns',
            'price': 150000.0,
            'daily_return_rate': 17.00,  # ₦25500 / ₦150000 * 100 = 17.00%
            'duration_days': 35
        },
        {
            'name': 'FF11',
            'description': 'Ultra package - Maximum returns',
            'price': 200000.0,
            'daily_return_rate': 25.25,  # ₦50500 / ₦200000 * 100 = 25.25%
            'duration_days': 35
        },
        {
            'name': 'FF12',
            'description': 'Supreme package - Ultimate returns',
            'price': 250000.0,
            'daily_return_rate': 22.28,  # ₦55700 / ₦250000 * 100 = 22.28%
            'duration_days': 35
        },
        {
            'name': 'FF13',
            'description': 'Master package - Legendary returns',
            'price': 300000.0,
            'daily_return_rate': 28.33,  # ₦85000 / ₦300000 * 100 = 28.33%
            'duration_days': 35
        }
    ]
    
    print("📦 Creating Fintech Finance packages...")
    for i, package_data in enumerate(packages, 1):
        package = Package(**package_data)
        db.session.add(package)
        
        # Calculate expected values for verification
        daily_income = (package_data['price'] * package_data['daily_return_rate']) / 100
        total_income = daily_income * package_data['duration_days']
        
        print(f"   ✅ {package_data['name']}: ₦{package_data['price']:,.0f} → ₦{daily_income:,.0f}/day → ₦{total_income:,.0f} total")
    
    db.session.commit()
    print("✅ All FF packages created successfully!")

def update_system_settings():
    """Update system-wide settings in the app configuration"""
    print("\n⚙️  System Settings:")
    print("   💰 Welcome Bonus: ₦700")
    print("   💳 Minimum Deposit: ₦3,000")
    print("   💸 Minimum Withdrawal: ₦1,000")
    print("   🎯 Daily Check-in: ₦200")
    print("   ⏰ Withdrawal Time: 9am - 6pm")
    print("   📊 Income Drops: Every 22 hours")
    print("\n🎯 Referral Commissions:")
    print("   📈 Level 1: 24%")
    print("   📈 Level 2: 4%")
    print("   📈 Level 3: 2%")

def verify_packages():
    """Verify that packages were created correctly"""
    print("\n🔍 Verifying packages...")
    
    packages = Package.query.order_by(Package.price).all()
    print(f"✅ Created {len(packages)} packages")
    
    print("\n📋 Package Summary:")
    print("PACKAGE | PRICE     | DAILY     | TOTAL      | DURATION")
    print("-" * 55)
    
    for package in packages:
        daily_income = package.daily_income
        total_income = package.total_return
        print(f"{package.name:<7} | ₦{package.price:>7,.0f} | ₦{daily_income:>7,.0f} | ₦{total_income:>9,.0f} | {package.duration_days} DAYS")

def main():
    """Main function to update the entire system"""
    print("🚀 Updating Fintech Finance System...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Clear and recreate packages
            clear_existing_packages()
            create_fintech_packages()
            
            # Display settings
            update_system_settings()
            
            # Verify creation
            verify_packages()
            
            print("\n🎉 Fintech Finance system updated successfully!")
            print("\n📋 Next Steps:")
            print("   1. Update app.py with new system settings")
            print("   2. Update referral commission rates")
            print("   3. Update minimum deposit/withdrawal amounts")
            print("   4. Test the packages in the web interface")
            
        except Exception as e:
            print(f"❌ Error updating system: {e}")

if __name__ == '__main__':
    main()
