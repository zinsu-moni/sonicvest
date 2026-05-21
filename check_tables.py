import sqlite3

conn = sqlite3.connect('instance/fintech.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Available tables:')
for table in tables:
    print(f'  - {table[0]}')
    
# Check if there's a withdrawal table
if any('withdrawal' in table[0].lower() for table in tables):
    print('\nFound withdrawal-related table!')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%withdrawal%'")
    withdrawal_tables = cursor.fetchall()
    for table in withdrawal_tables:
        print(f'Withdrawal table: {table[0]}')
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print('Columns:')
        for col in columns:
            print(f'  - {col[1]} ({col[2]})')

conn.close()
