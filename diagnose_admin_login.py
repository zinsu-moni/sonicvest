"""
Diagnose admin login issues
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import app
from app import app, db
from sqlalchemy import text

with app.app_context():
    print("=" * 60)
    print("🔍 ADMIN LOGIN DIAGNOSIS")
    print("=" * 60)
    
    # Check database connection
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    print(f"\n📊 Database: {database_url[:50]}...")
    
    try:
        # Check if admin_users table exists
        result = db.session.execute(text(
            "SELECT COUNT(*) FROM admin_users"
        )).scalar()
        print(f"✅ Admin users table exists")
        print(f"📋 Total admin users: {result}")
        
        # Get all admin users
        admins = db.session.execute(text(
            "SELECT id, username, email, is_active FROM admin_users"
        )).fetchall()
        
        if admins:
            print(f"\n📋 Existing Admin Users:")
            for admin in admins:
                status = "✅ Active" if admin[3] else "❌ Inactive"
                print(f"   ID: {admin[0]}, Username: {admin[1]}, Email: {admin[2]} - {status}")
        else:
            print(f"\n❌ No admin users found!")
            print("\n🔧 Creating default admin user...")
            
            from werkzeug.security import generate_password_hash
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
            print("✅ Admin user created successfully!")
            print("\n👤 Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTrying to create admin_users table...")
        
        try:
            db.session.execute(text('''
                CREATE TABLE IF NOT EXISTS admin_users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role VARCHAR(50) DEFAULT 'admin',
                    is_active BOOLEAN DEFAULT true,
                    last_login TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            db.session.commit()
            print("✅ Admin users table created!")
            
            # Now create admin user
            from werkzeug.security import generate_password_hash
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
            print("✅ Admin user created successfully!")
            print("\n👤 Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            
        except Exception as e2:
            print(f"❌ Failed to create table: {e2}")
