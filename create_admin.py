#!/usr/bin/env python3
"""
Create Admin User Script
This script creates an admin user for the Fintech Finance application.
"""

from app import app, db, User
from werkzeug.security import generate_password_hash
import sys

def create_admin_user():
    """Create an admin user"""
    
    print("🔧 Creating Admin User for Fintech Finance")
    print("=" * 50)
    
    # Get admin details
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    email = input("Enter admin email (default: admin@fintech.com): ").strip() or "admin@fintech.com"
    
    # Get password
    import getpass
    while True:
        password = getpass.getpass("Enter admin password: ").strip()
        if len(password) >= 6:
            confirm_password = getpass.getpass("Confirm password: ").strip()
            if password == confirm_password:
                break
            else:
                print("❌ Passwords don't match. Try again.")
        else:
            print("❌ Password must be at least 6 characters long.")
    
    try:
        with app.app_context():
            # Check if admin user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"❌ User with email {email} already exists!")
                
                # Ask if user wants to make existing user admin
                make_admin = input("Make this user an admin? (y/n): ").strip().lower()
                if make_admin == 'y':
                    existing_user.is_admin = True
                    db.session.commit()
                    print(f"✅ User {existing_user.name} is now an admin!")
                    return True
                else:
                    return False
            
            # Create new admin user
            admin_user = User(
                name=username,
                email=email,
                password_hash=generate_password_hash(password),
                phone="",
                is_admin=True,
                recharge_balance=0.0,
                main_balance=0.0
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"✅ Admin user created successfully!")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Admin ID: {admin_user.id}")
            print(f"   Referral Code: {admin_user.referral_code}")
            print()
            print("🎯 Admin Panel Access:")
            print(f"   URL: http://localhost:5000/admin")
            print(f"   Login with: {email}")
            print()
            print("⚠️  IMPORTANT: Keep these credentials secure!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

def list_admin_users():
    """List all admin users"""
    try:
        with app.app_context():
            admin_users = User.query.filter_by(is_admin=True).all()
            
            if not admin_users:
                print("📝 No admin users found.")
                return
            
            print(f"📝 Found {len(admin_users)} admin user(s):")
            print("-" * 60)
            for user in admin_users:
                status = "Active" if user.is_active else "Inactive"
                print(f"ID: {user.id} | {user.name} | {user.email} | {status}")
            
    except Exception as e:
        print(f"❌ Error listing admin users: {e}")

# Disabled auto execution to prevent prompts
# if __name__ == "__main__":
#     print("🚀 Fintech Finance Admin User Manager")
#     print()
#     
#     if len(sys.argv) > 1 and sys.argv[1] == "list":
#         list_admin_users()
#     else:
#         # Create admin user
#         success = create_admin_user()
#         
#         if success:
#             print()
#             print("🎉 Admin user setup complete!")
#             print("   You can now access the admin panel at /admin")
#         else:
#             print()
#             print("❌ Admin user setup failed!")
#             
#         print()
#         print("💡 Tips:")
#         print("   - Run 'python create_admin.py list' to see all admin users")
#         print("   - Access admin panel: http://localhost:5000/admin")
#         print("   - Use the same login as regular users, admin features will be available")
