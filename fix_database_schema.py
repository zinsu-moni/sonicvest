"""
Database Migration Script - Fix Missing Columns
This script adds missing columns to existing database tables
Run this if you get "no such column" errors
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add missing columns to existing database tables"""
    
    print("=" * 60)
    print("🔧 Database Migration - Adding Missing Columns")
    print("=" * 60)
    
    # Find database file
    db_paths = ['fintech.db', 'instance/fintech.db']
    db_path = None
    
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ Database file not found!")
        print("💡 Database will be created automatically on first app run")
        return False
    
    print(f"\n📁 Found database: {db_path}")
    
    try:
        # Backup database first
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # ==================== USER TABLE ====================
        print("\n📋 Migrating 'user' table...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(user)")
            user_columns = [col[1] for col in cursor.fetchall()]
            
            user_migrations = [
                ('is_admin', 'BOOLEAN DEFAULT 0'),
                ('bank_name', 'VARCHAR(100)'),
                ('account_number', 'VARCHAR(50)'),
                ('account_name', 'VARCHAR(100)'),
                ('last_checkin', 'DATETIME')
            ]
            
            for col_name, col_type in user_migrations:
                if col_name not in user_columns:
                    try:
                        cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} {col_type}")
                        print(f"  ✅ Added: user.{col_name}")
                    except Exception as e:
                        print(f"  ⚠️  user.{col_name}: {e}")
                else:
                    print(f"  ℹ️  Skipped: user.{col_name} (already exists)")
        else:
            print("  ⚠️  Table 'user' not found")
        
        # ==================== USER_PACKAGE TABLE ====================
        print("\n📋 Migrating 'user_package' table...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_package'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(user_package)")
            package_columns = [col[1] for col in cursor.fetchall()]
            
            package_migrations = [
                ('purchase_date', 'DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'),
                ('expiry_date', 'DATETIME'),
                ('amount_invested', 'FLOAT DEFAULT 0'),
                ('start_date', 'DATETIME DEFAULT CURRENT_TIMESTAMP'),
                ('end_date', 'DATETIME'),
                ('daily_return', 'FLOAT DEFAULT 0'),
                ('total_earned', 'FLOAT DEFAULT 0'),
                ('last_payout', 'DATETIME'),
                ('is_active', 'BOOLEAN DEFAULT 1')
            ]
            
            for col_name, col_type in package_migrations:
                if col_name not in package_columns:
                    try:
                        cursor.execute(f"ALTER TABLE user_package ADD COLUMN {col_name} {col_type}")
                        print(f"  ✅ Added: user_package.{col_name}")
                    except Exception as e:
                        print(f"  ⚠️  user_package.{col_name}: {e}")
                else:
                    print(f"  ℹ️  Skipped: user_package.{col_name} (already exists)")
        else:
            print("  ⚠️  Table 'user_package' not found")
        
        # ==================== WITHDRAWAL TABLE ====================
        print("\n📋 Migrating 'withdrawal' table...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='withdrawal'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(withdrawal)")
            withdrawal_columns = [col[1] for col in cursor.fetchall()]
            
            withdrawal_migrations = [
                ('fee_amount', 'FLOAT DEFAULT 0'),
                ('net_amount', 'FLOAT DEFAULT 0'),
                ('admin_notes', 'TEXT'),
                ('processed_by', 'INTEGER'),
                ('processed_at', 'DATETIME')
            ]
            
            for col_name, col_type in withdrawal_migrations:
                if col_name not in withdrawal_columns:
                    try:
                        cursor.execute(f"ALTER TABLE withdrawal ADD COLUMN {col_name} {col_type}")
                        print(f"  ✅ Added: withdrawal.{col_name}")
                    except Exception as e:
                        print(f"  ⚠️  withdrawal.{col_name}: {e}")
                else:
                    print(f"  ℹ️  Skipped: withdrawal.{col_name} (already exists)")
        else:
            print("  ⚠️  Table 'withdrawal' not found")
        
        # ==================== DEPOSIT TABLE ====================
        print("\n📋 Migrating 'deposit' table...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='deposit'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(deposit)")
            deposit_columns = [col[1] for col in cursor.fetchall()]
            
            deposit_migrations = [
                ('admin_notes', 'TEXT'),
                ('processed_by', 'INTEGER'),
                ('processed_at', 'DATETIME'),
                ('receipt_path', 'VARCHAR(255)')
            ]
            
            for col_name, col_type in deposit_migrations:
                if col_name not in deposit_columns:
                    try:
                        cursor.execute(f"ALTER TABLE deposit ADD COLUMN {col_name} {col_type}")
                        print(f"  ✅ Added: deposit.{col_name}")
                    except Exception as e:
                        print(f"  ⚠️  deposit.{col_name}: {e}")
                else:
                    print(f"  ℹ️  Skipped: deposit.{col_name} (already exists)")
        else:
            print("  ⚠️  Table 'deposit' not found (may not be created yet)")
        
        # Commit all changes
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print(f"\n💾 Backup saved at: {backup_path}")
        print("🚀 You can now run the application")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        
        print(f"\n💡 Restore backup if needed:")
        print(f"   copy {backup_path} {db_path}")
        
        return False

if __name__ == '__main__':
    import sys
    
    print("\n⚠️  This script will modify your database")
    print("A backup will be created automatically\n")
    
    confirm = input("Continue with migration? (y/n): ").lower().strip()
    
    if confirm == 'y':
        success = migrate_database()
        sys.exit(0 if success else 1)
    else:
        print("\n❌ Migration cancelled")
        sys.exit(1)
