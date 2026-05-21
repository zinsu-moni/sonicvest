#!/usr/bin/env python3
"""Standalone database checker - no imports from app"""

import sqlite3
import os
import sys

def check_database():
    try:
        # Get the database path
        db_path = os.path.join('instance', 'fintech.db')
        print(f"Checking database: {db_path}")
        
        if not os.path.exists(db_path):
            print("❌ Database file not found!")
            return False
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
        if not cursor.fetchone():
            print("❌ User table not found!")
            conn.close()
            return False
        
        # Get table schema
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        print("✅ Database found and accessible")
        print("\nCurrent user table columns:")
        column_names = []
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            column_names.append(col[1])
        
        # Check for required columns
        required_columns = ['is_admin', 'bank_name', 'account_number', 'account_name']
        missing_columns = []
        
        for col in required_columns:
            if col not in column_names:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"\n❌ Missing columns: {missing_columns}")
            print("Adding missing columns...")
            
            for col in missing_columns:
                try:
                    if col == 'is_admin':
                        cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
                    elif col == 'bank_name':
                        cursor.execute("ALTER TABLE user ADD COLUMN bank_name VARCHAR(100)")
                    elif col == 'account_number':
                        cursor.execute("ALTER TABLE user ADD COLUMN account_number VARCHAR(50)")
                    elif col == 'account_name':
                        cursor.execute("ALTER TABLE user ADD COLUMN account_name VARCHAR(100)")
                    
                    print(f"  ✅ Added {col}")
                except Exception as e:
                    print(f"  ❌ Failed to add {col}: {e}")
            
            conn.commit()
            print("\n🎉 Database migration completed!")
        else:
            print("\n✅ All required columns exist!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_database()
