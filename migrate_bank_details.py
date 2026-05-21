#!/usr/bin/env python3
"""
Database migration script to add bank details to existing user table.
This fixes the 'no such column: user.bank_name' error.
"""

import sqlite3
import os
from app import app, db

def migrate_database():
    """Add missing bank details columns to the user table"""
    
    # Path to the database file
    db_path = os.path.join(os.getcwd(), 'instance', 'fintech.db')
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        print("💡 Creating new database with all columns...")
        
        # Create new database with app context
        with app.app_context():
            db.create_all()
            print("✅ New database created successfully!")
        return True
    
    print(f"🔧 Migrating existing database: {db_path}")
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if bank_name column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"📋 Existing columns: {columns}")
        
        # Add missing columns if they don't exist
        missing_columns = []
        
        if 'bank_name' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN bank_name VARCHAR(100)")
            missing_columns.append('bank_name')
            print("   ✅ Added bank_name column")
        
        if 'account_number' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN account_number VARCHAR(20)")
            missing_columns.append('account_number')
            print("   ✅ Added account_number column")
        
        if 'account_name' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN account_name VARCHAR(100)")
            missing_columns.append('account_name')
            print("   ✅ Added account_name column")
        
        if missing_columns:
            conn.commit()
            print(f"✅ Successfully added columns: {missing_columns}")
        else:
            print("✅ All columns already exist, no migration needed")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def verify_migration():
    """Verify that the migration was successful"""
    print("\n🔍 Verifying migration...")
    
    try:
        with app.app_context():
            # Try to create a test query that uses the new columns
            from app import User
            
            # This should work without errors now
            user_count = User.query.count()
            print(f"✅ Database verification successful! Found {user_count} users")
            
            # Test accessing bank fields on existing users
            if user_count > 0:
                first_user = User.query.first()
                print(f"   👤 Test user: {first_user.name}")
                print(f"   🏦 Bank name: {first_user.bank_name or 'Not set'}")
                print(f"   💳 Account: {first_user.account_number or 'Not set'}")
            
            return True
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting database migration...")
    
    # Perform migration
    if migrate_database():
        # Verify migration
        if verify_migration():
            print("\n🎉 Migration completed successfully!")
            print("💡 You can now restart your Flask application")
        else:
            print("\n⚠️  Migration completed but verification failed")
    else:
        print("\n❌ Migration failed")
