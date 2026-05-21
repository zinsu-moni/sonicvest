#!/usr/bin/env python3
"""
Test the password reset functionality
"""

from app import app, db, User
from werkzeug.security import generate_password_hash, check_password_hash

def test_password_reset():
    """Test the password reset functionality"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if test user exists
        test_user = User.query.filter_by(email='test@fintech.com').first()
        
        if not test_user:
            print("👤 Creating test user for password reset demo...")
            test_user = User(
                name='Test User',
                email='test@fintech.com',
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
            print("✅ Test user created!")
        
        print(f"\n🔐 Password Reset Test User:")
        print(f"   📧 Email: test@fintech.com")
        print(f"   🔑 Password: password123")
        print(f"   💰 Balance: ₦{test_user.balance:,.0f}")
        print(f"   🏦 Bank: {test_user.bank_name}")
        
        # Test password verification
        current_password = 'password123'
        is_valid = check_password_hash(test_user.password_hash, current_password)
        print(f"   ✅ Password verification: {'✓ Valid' if is_valid else '✗ Invalid'}")
        
        print(f"\n🌐 To test password reset:")
        print(f"   1. Start the app: python app.py")
        print(f"   2. Login with: test@fintech.com / password123")
        print(f"   3. Go to Profile → Security Manager")
        print(f"   4. Change your password")
        print(f"   5. Login again with new password")

if __name__ == '__main__':
    test_password_reset()
