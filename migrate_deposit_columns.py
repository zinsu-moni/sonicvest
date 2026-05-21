#!/usr/bin/env python3
"""
Migration script to add status and reference columns to transaction table
for the manual deposit system.
"""

import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'fintech.db')

def migrate():
    """Add status and reference columns to transaction table"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(\"transaction\")")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"Current transaction table columns: {columns}")
        
        # Add status column if it doesn't exist
        if 'status' not in columns:
            print("Adding 'status' column to transaction table...")
            cursor.execute('''
                ALTER TABLE "transaction" 
                ADD COLUMN status VARCHAR(50) DEFAULT 'completed'
            ''')
            print("✅ 'status' column added")
        else:
            print("✓ 'status' column already exists")
        
        # Add reference column if it doesn't exist
        if 'reference' not in columns:
            print("Adding 'reference' column to transaction table...")
            cursor.execute('''
                ALTER TABLE "transaction" 
                ADD COLUMN reference VARCHAR(50) UNIQUE
            ''')
            print("✅ 'reference' column added")
        else:
            print("✓ 'reference' column already exists")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Running migration script...")
    print(f"Database: {DATABASE_PATH}\n")
    migrate()
