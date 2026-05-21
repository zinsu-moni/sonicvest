#!/usr/bin/env python3
"""
Database Migration Script
Adds missing columns to the user table
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add missing columns to the database"""
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'fintech.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    print(f"Migrating database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current table structure
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Current user table columns: {columns}")
        
        # Add missing columns if they don't exist
        migrations_applied = []
        
        # Add is_admin column
        if 'is_admin' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0')
            migrations_applied.append('is_admin')
            print("✅ Added is_admin column")
        
        # Add bank details columns if they don't exist
        if 'bank_name' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN bank_name TEXT')
            migrations_applied.append('bank_name')
            print("✅ Added bank_name column")
        
        if 'account_number' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN account_number TEXT')
            migrations_applied.append('account_number')
            print("✅ Added account_number column")
        
        if 'account_name' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN account_name TEXT')
            migrations_applied.append('account_name')
            print("✅ Added account_name column")
        
        # Add main_balance column if it doesn't exist (some systems may have income_balance instead)
        if 'main_balance' not in columns:
            # Check if income_balance exists, if so rename it
            if 'income_balance' in columns:
                # SQLite doesn't support column rename directly, so we'll add the new column and copy data
                cursor.execute('ALTER TABLE user ADD COLUMN main_balance REAL DEFAULT 0.0')
                cursor.execute('UPDATE user SET main_balance = income_balance')
                migrations_applied.append('main_balance (copied from income_balance)')
                print("✅ Added main_balance column and copied data from income_balance")
            else:
                cursor.execute('ALTER TABLE user ADD COLUMN main_balance REAL DEFAULT 0.0')
                migrations_applied.append('main_balance')
                print("✅ Added main_balance column")
        
        # Commit changes
        conn.commit()
        
        # Verify changes
        cursor.execute("PRAGMA table_info(user)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"Updated user table columns: {new_columns}")
        
        # Create a test admin user if none exists
        cursor.execute('SELECT COUNT(*) FROM user WHERE is_admin = 1')
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            from werkzeug.security import generate_password_hash
            import secrets
            
            # Generate unique referral code
            referral_code = secrets.token_urlsafe(6)[:8].upper()
            password_hash = generate_password_hash('admin123')
            
            cursor.execute('''
                INSERT INTO user (name, email, password_hash, referral_code, is_admin, recharge_balance, main_balance, total_earned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Admin User', 'admin@fintech.com', password_hash, referral_code, 1, 100000.0, 0.0, 0.0))
            
            conn.commit()
            print("✅ Created admin user: admin@fintech.com / admin123")
        
        conn.close()
        
        if migrations_applied:
            print(f"\n🎉 Migration completed successfully!")
            print(f"Applied migrations: {', '.join(migrations_applied)}")
        else:
            print("✅ No migrations needed - database is up to date")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    print("🔄 Starting database migration...")
    success = migrate_database()
    
    if success:
        print("\n✅ Database migration completed successfully!")
        print("You can now run the Flask application.")
    else:
        print("\n❌ Database migration failed!")
        print("Please check the error messages above.")
