#!/usr/bin/env python3
"""
Quick Admin Creation Script - No Input Required
"""

import sys
import os
sys.path.append(os.getcwd())

from app import app, db, User
from werkzeug.security import generate_password_hash

def create_quick_admin():
    """Create an admin user with predefined credentials"""
    
    with app.app_context():
        # Check if admin already exists
        admin_user = User.query.filter_by(email='admin@fintech.com').first()
        
        if admin_user:
            # Update existing user to be admin
            admin_user.is_admin = True
            db.session.commit()
            print("✅ Updated existing user to admin")
            print(f"   Email: admin@fintech.com")
            print(f"   Username: {admin_user.name}")
        else:
            # Create new admin user
            admin_user = User(
                name='admin',
                email='admin@fintech.com',
                password_hash=generate_password_hash('admin123'),
                phone='1234567890',
                recharge_balance=0.0,
                main_balance=0.0,
                total_earned=0.0,
                is_admin=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Created new admin user")
        
        print("\n🔑 Admin Login Credentials:")
        print("   Email: admin@fintech.com")
        print("   Password: admin123")
        print("\n🌐 Access URLs:")
        print("   Main Site: http://127.0.0.1:5000")
        print("   Admin Panel: http://127.0.0.1:5000/admin")
        print("\n💡 Note: Log in with these credentials on the main site first,")
        print("   then visit the admin panel URL.")

if __name__ == "__main__":
    try:
        create_quick_admin()
    except Exception as e:
        print(f"❌ Error: {e}")
