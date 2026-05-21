#!/usr/bin/env python3
"""
Simple database reset and setup script.
This will recreate the database with all the correct columns.
"""

import os
from app import app, db, Package, User
from werkzeug.security import generate_password_hash

def reset_database():
    """Remove old database and create fresh one with correct schema"""
    
    # Remove old database files
    db_files = ['fintech.db', 'instance/fintech.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"🗑️  Removed old database: {db_file}")
    
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    print("🔨 Creating fresh database...")
    
    with app.app_context():
        # Create all tables with correct schema
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default packages
        create_default_packages()
        
        # Create test user
        create_test_user()
        
        print("🎉 Database setup complete!")

def create_default_packages():
    """Create default investment packages"""
    packages = [
        {
            'name': 'Starter Package',
            'description': 'Perfect for beginners - Low risk, steady returns',
            'price': 5000.0,
            'daily_return_rate': 2.86,
            'duration_days': 30
        },
        {
            'name': 'Silver Package', 
            'description': 'Balanced investment with moderate returns',
            'price': 15000.0,
            'daily_return_rate': 3.25,
            'duration_days': 30
        },
        {
            'name': 'Gold Package',
            'description': 'Premium investment with higher returns',
            'price': 50000.0,
            'daily_return_rate': 3.75,
            'duration_days': 30
        },
        {
            'name': 'Platinum Package',
            'description': 'Elite investment for serious investors',
            'price': 100000.0,
            'daily_return_rate': 4.25,
            'duration_days': 30
        }
    ]
    
    print("📦 Creating investment packages...")
    for package_data in packages:
        package = Package(**package_data)
        db.session.add(package)
        print(f"   ✅ {package_data['name']} - ₦{package_data['price']:,.0f}")
    
    db.session.commit()

def create_test_user():
    """Create test user with bank details"""
    print("👤 Creating test user...")
    
    test_user = User(
        name='Demo User',
        email='demo@fintech.com',
        password_hash=generate_password_hash('demo123'),
        phone='+234800000000',
        recharge_balance=25000.0,
        main_balance=10000.0,
        bank_name='GTBank',
        account_number='0123456789',
        account_name='Demo User'
    )
    
    db.session.add(test_user)
    db.session.commit()
    
    print(f"   ✅ Demo user created:")
    print(f"   📧 Email: demo@fintech.com")
    print(f"   🔐 Password: demo123")
    print(f"   💰 Recharge Balance: ₦{test_user.recharge_balance:,.0f}")
    print(f"   💰 Main Balance: ₦{test_user.main_balance:,.0f}")
    print(f"   🔗 Referral Code: {test_user.referral_code}")
    print(f"   🏦 Bank: {test_user.bank_name} - {test_user.account_number}")

if __name__ == '__main__':
    print("🚀 Resetting database with fresh schema...")
    reset_database()
    print("\n📋 Quick Start:")
    print("1. Run: python app.py")
    print("2. Visit: http://127.0.0.1:5000")
    print("3. Login: demo@fintech.com / demo123")
    print("4. Explore the platform!")
