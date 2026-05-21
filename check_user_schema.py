#!/usr/bin/env python3
"""Check user table schema"""

import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'fintech.db')

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Check user table columns
cursor.execute('PRAGMA table_info("user")')
user_columns = [col[1] for col in cursor.fetchall()]
print(f"User table columns: {user_columns}")

# Check transaction table columns
cursor.execute('PRAGMA table_info("transaction")')
txn_columns = [col[1] for col in cursor.fetchall()]
print(f"Transaction table columns: {txn_columns}")

# Check if user has balance column
if 'balance' in user_columns:
    print("✓ User table has 'balance' column")
else:
    print("✗ User table is MISSING 'balance' column - this needs to be fixed!")

conn.close()
