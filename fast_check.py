import sqlite3
import sys

try:
    conn = sqlite3.connect('fintech.db', timeout=5)
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f'Found {len(tables)} tables:')
    for t in tables:
        print(f'  - {t[0]}')
    
    # Check user table specifically
    if any('user' in str(t) for t in tables):
        user_count = cursor.execute("SELECT COUNT(*) FROM user").fetchone()[0]
        print(f'User table has {user_count} records')
    
    conn.close()
    print("✅ Database check completed")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
