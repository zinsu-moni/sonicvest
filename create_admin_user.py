#!/usr/bin/env python
"""
Create or reset admin user in the database
Run: python create_admin_user.py
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

def create_admin_user():
    """Create or update admin user"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Import app
        from app import app, db
        
        with app.app_context():
            print("=" * 60)
            print("👤 ADMIN USER SETUP")
            print("=" * 60)
            
            # Check database connection
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            print(f"\n📊 Database: {database_url[:50]}...")
            
            from sqlalchemy import text
            
            # Check if admin_users table exists
            try:
                result = db.session.execute(text(
                    "SELECT COUNT(*) FROM admin_users"
                )).scalar()
                print(f"✅ Admin users table exists ({result} users)")
            except Exception as e:
                print(f"❌ Admin table error: {e}")
                return
            
            # Check existing admin
            try:
                existing = db.session.execute(text(
                    "SELECT id, username, email FROM admin_users WHERE username = 'admin'"
                )).fetchone()
                
                if existing:
                    print(f"\n✅ Admin user exists:")
                    print(f"   ID: {existing[0]}")
                    print(f"   Username: {existing[1]}")
                    print(f"   Email: {existing[2]}")
                    
                    # Ask to reset password
                    response = input("\n🔑 Reset admin password? (y/n): ").strip().lower()
                    if response == 'y':
                        admin_password = generate_password_hash('admin123')
                        db.session.execute(text(
                            "UPDATE admin_users SET password_hash = :hash WHERE username = 'admin'"
                        ), {'hash': admin_password})
                        db.session.commit()
                        print("✅ Password reset to: admin123")
                else:
                    print("\n❌ Admin user not found. Creating...")
                    admin_password = generate_password_hash('admin123')
                    
                    db.session.execute(text('''
                        INSERT INTO admin_users (username, email, password_hash, role, is_active)
                        VALUES (:username, :email, :password, :role, :is_active)
                    '''), {
                        'username': 'admin',
                        'email': 'admin@fintech.com',
                        'password': admin_password,
                        'role': 'super_admin',
                        'is_active': True
                    })
                    db.session.commit()
                    print("✅ Admin user created:")
                    print("   Username: admin")
                    print("   Password: admin123")
                    print("   Email: admin@fintech.com")
            except Exception as e:
                print(f"❌ Error: {e}")
                db.session.rollback()
                return
            
            print("\n" + "=" * 60)
            print("✅ ADMIN USER READY")
            print("=" * 60)
            print("\n🚀 Login at: http://localhost:5000/admin/login")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    create_admin_user()
