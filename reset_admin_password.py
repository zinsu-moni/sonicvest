"""
Reset admin password to default
"""
import os
import sys
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

from app import app, db
from sqlalchemy import text

with app.app_context():
    print("=" * 60)
    print("🔑 RESET ADMIN PASSWORD")
    print("=" * 60)
    
    try:
        # Reset password to admin123
        new_password = generate_password_hash('admin123')
        
        db.session.execute(text(
            "UPDATE admin_users SET password_hash = :hash WHERE username = 'admin'"
        ), {'hash': new_password})
        
        db.session.commit()
        
        print("\n✅ Admin password reset successfully!")
        print("\n👤 Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Login at: http://localhost:5000/admin/login")
        
    except Exception as e:
        print(f"❌ Error: {e}")
