#!/usr/bin/env python
"""
Diagnose admin user and login issues
"""

import os
import sys
from dotenv import load_dotenv

# Load .env file first
load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

def diagnose_admin():
    """Diagnose admin login issues"""
    try:
        from app import app, db
        from werkzeug.security import check_password_hash
        from sqlalchemy import text
        
        with app.app_context():
            print("=" * 70)
            print("🔍 ADMIN LOGIN DIAGNOSTICS")
            print("=" * 70)
            
            # Check which database is being used
            db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            print(f"\n📍 Database: {db_url.split('@')[0] if '@' in db_url else db_url[:50]}")
            
            is_postgresql = 'postgresql' in db_url
            print(f"   Type: {'PostgreSQL' if is_postgresql else 'SQLite'}")
            
            # 1. Check if admin_users table exists
            print("\n1️⃣  Checking admin_users table...")
            try:
                if is_postgresql:
                    result = db.session.execute(text(
                        "SELECT table_name FROM information_schema.tables WHERE table_name='admin_users'"
                    )).fetchone()
                else:
                    # SQLite query
                    result = db.session.execute(text(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name='admin_users'"
                    )).fetchone()
                
                if result:
                    print("   ✅ admin_users table exists")
                else:
                    print("   ❌ admin_users table NOT found")
                    return
            except Exception as e:
                print(f"   ❌ Error checking table: {e}")
                return
            
            # 2. Count admin users
            print("\n2️⃣  Checking admin users...")
            try:
                count = db.session.execute(text(
                    "SELECT COUNT(*) FROM admin_users"
                )).scalar()
                print(f"   ✅ Found {count} admin users")
                
                if count == 0:
                    print("   ⚠️  No admin users found! Creating default admin...")
                    from werkzeug.security import generate_password_hash
                    from datetime import datetime
                    
                    admin_password = generate_password_hash('admin123')
                    db.session.execute(text('''
                        INSERT INTO admin_users (username, email, password_hash, role, created_at, is_active)
                        VALUES (:username, :email, :password, :role, :created_at, :is_active)
                    '''), {
                        'username': 'admin',
                        'email': 'admin@fintech.com',
                        'password': admin_password,
                        'role': 'super_admin',
                        'created_at': datetime.now(),
                        'is_active': True
                    })
                    db.session.commit()
                    print("   ✅ Default admin created!")
                    count = 1
            except Exception as e:
                print(f"   ❌ Error: {e}")
                db.session.rollback()
                return
            
            # 3. List all admin users
            print("\n3️⃣  Listing admin users...")
            try:
                admins = db.session.execute(text(
                    "SELECT id, username, email, role, is_active, created_at FROM admin_users"
                )).fetchall()
                
                for admin in admins:
                    print(f"   ID: {admin[0]}")
                    print(f"   Username: {admin[1]}")
                    print(f"   Email: {admin[2]}")
                    print(f"   Role: {admin[3]}")
                    print(f"   Active: {admin[4]}")
                    print(f"   Created: {admin[5]}")
                    print()
            except Exception as e:
                print(f"   ❌ Error: {e}")
                return
            
            # 4. Test password hash
            print("\n4️⃣  Testing password verification...")
            try:
                admin = db.session.execute(text(
                    "SELECT username, password_hash FROM admin_users WHERE username='admin' LIMIT 1"
                )).fetchone()
                
                if admin:
                    username, password_hash = admin[0], admin[1]
                    test_password = 'admin123'
                    
                    is_correct = check_password_hash(password_hash, test_password)
                    
                    print(f"   Username: {username}")
                    print(f"   Password hash exists: {bool(password_hash)}")
                    print(f"   Password 'admin123' matches: {is_correct}")
                    
                    if not is_correct:
                        print("   ⚠️  Password mismatch! Resetting password...")
                        from werkzeug.security import generate_password_hash
                        new_hash = generate_password_hash('admin123')
                        db.session.execute(text(
                            "UPDATE admin_users SET password_hash = :hash WHERE username = 'admin'"
                        ), {'hash': new_hash})
                        db.session.commit()
                        print("   ✅ Password reset to 'admin123'")
                else:
                    print("   ❌ No admin user found")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # 5. Test database connection
            print("\n5️⃣  Testing database query...")
            try:
                admin = db.session.execute(text(
                    "SELECT id, username, email FROM admin_users WHERE username = :username AND is_active = true"
                ), {'username': 'admin'}).fetchone()
                
                if admin:
                    print(f"   ✅ Query successful")
                    print(f"   Admin ID: {admin[0]}")
                    print(f"   Username: {admin[1]}")
                    print(f"   Email: {admin[2]}")
                else:
                    print("   ⚠️  Query returned no results")
            except Exception as e:
                print(f"   ❌ Query error: {e}")
                db.session.rollback()
            
            print("\n" + "=" * 70)
            print("✅ DIAGNOSTICS COMPLETE")
            print("=" * 70)
            print("\n🔑 Admin Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\nTry logging in at: http://localhost:5000/admin/login")
            print("\n")
            
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_admin()
