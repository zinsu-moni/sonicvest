#!/usr/bin/env python
"""
Setup script for admin user and logging
Run: python setup_admin.py
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

def setup_admin():
    """Setup admin database and user"""
    try:
        # Import app
        from app import app, db
        
        with app.app_context():
            print("=" * 60)
            print("🔧 ADMIN SETUP SCRIPT")
            print("=" * 60)
            
            # Create all tables
            print("\n📦 Creating database tables...")
            db.create_all()
            print("✅ Database tables created")
            
            # Initialize admin database
            print("\n👤 Initializing admin user...")
            try:
                from admin_routes import init_admin_db
                init_admin_db()
                print("✅ Admin database initialized")
            except Exception as e:
                print(f"⚠️  Admin initialization: {e}")
            
            # Check admin user
            from sqlalchemy import text
            try:
                result = db.session.execute(text("SELECT COUNT(*) FROM admin_users")).scalar()
                if result > 0:
                    print(f"✅ Admin users exist: {result}")
                    
                    # List admin users
                    admins = db.session.execute(text(
                        "SELECT id, username, email, role, last_login FROM admin_users"
                    )).fetchall()
                    
                    print("\n📋 Admin Users:")
                    print("-" * 60)
                    for admin in admins:
                        print(f"  ID: {admin[0]}")
                        print(f"  Username: {admin[1]}")
                        print(f"  Email: {admin[2]}")
                        print(f"  Role: {admin[3]}")
                        print(f"  Last Login: {admin[4]}")
                        print("-" * 60)
                else:
                    print("⚠️  No admin users found. Creating default admin...")
                    admin_password = generate_password_hash('admin123')
                    db.session.execute(text('''
                        INSERT INTO admin_users (username, email, password_hash, role)
                        VALUES (:username, :email, :password, :role)
                    '''), {
                        'username': 'admin',
                        'email': 'admin@fintech.com',
                        'password': admin_password,
                        'role': 'super_admin'
                    })
                    db.session.commit()
                    print("✅ Default admin user created")
                    print("   Username: admin")
                    print("   Password: admin123")
            except Exception as e:
                print(f"❌ Admin check error: {e}")
                db.session.rollback()
            
            # Create admin log table if it doesn't exist
            print("\n📁 Setting up admin logs table...")
            try:
                db.session.execute(text('''
                    CREATE TABLE IF NOT EXISTS admin_logs (
                        id SERIAL PRIMARY KEY,
                        admin_id INTEGER,
                        action VARCHAR(255) NOT NULL,
                        target_type VARCHAR(100),
                        target_id INTEGER,
                        details TEXT,
                        ip_address VARCHAR(45),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (admin_id) REFERENCES admin_users(id) ON DELETE SET NULL
                    )
                '''))
                db.session.commit()
                print("✅ Admin logs table created")
            except Exception as e:
                print(f"⚠️  Admin logs table: {e}")
                db.session.rollback()
            
            # Create audit log table
            print("\n📊 Setting up audit logs table...")
            try:
                db.session.execute(text('''
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER,
                        action VARCHAR(255) NOT NULL,
                        resource_type VARCHAR(100),
                        resource_id INTEGER,
                        changes TEXT,
                        ip_address VARCHAR(45),
                        user_agent TEXT,
                        status VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL
                    )
                '''))
                db.session.commit()
                print("✅ Audit logs table created")
            except Exception as e:
                print(f"⚠️  Audit logs table: {e}")
                db.session.rollback()
            
            print("\n" + "=" * 60)
            print("✅ ADMIN SETUP COMPLETE")
            print("=" * 60)
            print("\n🚀 Next steps:")
            print("1. Run the Flask app: python app.py")
            print("2. Access admin panel: http://localhost:5000/admin")
            print("3. Login with: admin / admin123")
            print("\n")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    setup_admin()
