#!/usr/bin/env python3
"""
Database initialization script for the Fintech application.
Creates default packages and sets up the database.
"""

from app import app, db, Package, User
from werkzeug.security import generate_password_hash

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
        },
        {
            'name': 'Diamond Package',
            'description': 'Ultimate investment package - Maximum returns',
            'price': 250000.0,
            'daily_return_rate': 5.0,
            'duration_days': 30
        }
    ]
    
    print("🎁 Creating default packages...")
    for package_data in packages:
        # Check if package already exists
        existing = Package.query.filter_by(name=package_data['name']).first()
        if not existing:
            package = Package(**package_data)
            db.session.add(package)
            print(f"   ✅ Created: {package_data['name']} (₦{package_data['price']:,.0f})")
        else:
            print(f"   ⏭️  Exists: {package_data['name']}")
    
    db.session.commit()
    print("✅ Packages setup complete!")

def create_test_user():
    """Create a test user for development"""
    test_email = 'test@fintech.com'
    existing_user = User.query.filter_by(email=test_email).first()
    
    if not existing_user:
        print("👤 Creating test user...")
        test_user = User(
            name='Test User',
            email=test_email,
            password_hash=generate_password_hash('password123'),
            phone='+234800000000',
            recharge_balance=10000.0,
            main_balance=5000.0,
            bank_name='Test Bank',
            account_number='1234567890',
            account_name='Test User'
        )
        
        db.session.add(test_user)
        db.session.commit()
        
        print(f"   ✅ Test user created:")
        print(f"   📧 Email: {test_email}")
        print(f"   🔐 Password: password123")
        print(f"   💰 Recharge Balance: ₦{test_user.recharge_balance:,.0f}")
        print(f"   💰 Main Balance: ₦{test_user.main_balance:,.0f}")
        print(f"   🔗 Referral Code: {test_user.referral_code}")
    else:
        print(f"   ⏭️  Test user already exists: {test_email}")

def setup_database():
    """Setup the complete database"""
    print("🗄️  Setting up database...")
    
    try:
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Create default data
        create_default_packages()
        create_test_user()
        
        print("\n🎉 Database setup complete!")
        print("\n📋 Quick Start Guide:")
        print("   1. Run: python app.py")
        print("   2. Open: http://127.0.0.1:5000")
        print("   3. Login with: test@fintech.com / password123")
        print("   4. Explore the dashboard and features")
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        print("💡 Make sure you're in the correct directory")
        return False
    
    return True

if __name__ == '__main__':
    with app.app_context():
        setup_database()
