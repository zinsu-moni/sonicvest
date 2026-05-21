"""
Add missing purchase_date and expiry_date columns to user_package table
"""
import sqlite3
import os
from datetime import datetime

db_path = 'fintech.db'

if not os.path.exists(db_path):
    print("❌ Database not found")
    exit(1)

print("🔧 Adding missing columns to user_package table...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check current columns
    cursor.execute("PRAGMA table_info(user_package)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\nCurrent columns: {', '.join(columns)}")
    
    # Add purchase_date if missing
    if 'purchase_date' not in columns:
        cursor.execute("ALTER TABLE user_package ADD COLUMN purchase_date DATETIME")
        print("✅ Added purchase_date column")
        
        # Update existing rows with start_date value
        cursor.execute("UPDATE user_package SET purchase_date = start_date WHERE purchase_date IS NULL")
        print("✅ Updated existing rows with purchase_date = start_date")
    else:
        print("ℹ️  purchase_date already exists")
    
    # Add expiry_date if missing
    if 'expiry_date' not in columns:
        cursor.execute("ALTER TABLE user_package ADD COLUMN expiry_date DATETIME")
        print("✅ Added expiry_date column")
        
        # Update existing rows with end_date value
        cursor.execute("UPDATE user_package SET expiry_date = end_date WHERE expiry_date IS NULL")
        print("✅ Updated existing rows with expiry_date = end_date")
    else:
        print("ℹ️  expiry_date already exists")
    
    conn.commit()
    
    # Verify
    cursor.execute("PRAGMA table_info(user_package)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n✅ Updated columns: {', '.join(columns)}")
    
    print("\n🎉 Successfully added missing columns!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
