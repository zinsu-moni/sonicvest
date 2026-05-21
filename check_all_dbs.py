import sqlite3
import os

# Check both database locations
db_locations = [
    'fintech.db',
    'instance/fintech.db'
]

for db_path in db_locations:
    if os.path.exists(db_path):
        print(f"\n🗄️  Database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        
        # Check if withdrawal table exists and its structure
        if any('withdrawal' in t[0] for t in tables):
            cursor.execute("PRAGMA table_info(withdrawal)")
            columns = cursor.fetchall()
            print("Withdrawal table columns:")
            for col in columns:
                print(f"  {col[1]} - {col[2]}")
        
        conn.close()
    else:
        print(f"❌ Database not found: {db_path}")
