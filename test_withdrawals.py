import sqlite3

# Connect to database and check withdrawal records
conn = sqlite3.connect('instance/fintech.db')
cursor = conn.cursor()

print("Checking withdrawal table...")
try:
    cursor.execute('SELECT COUNT(*) FROM withdrawal')
    count = cursor.fetchone()[0]
    print(f"Total withdrawal records: {count}")
    
    if count > 0:
        cursor.execute('SELECT * FROM withdrawal LIMIT 5')
        withdrawals = cursor.fetchall()
        print("\nSample withdrawal records:")
        for w in withdrawals:
            print(f"  ID: {w[0]}, User: {w[1]}, Amount: {w[2]}, Status: {w[8]}")
    else:
        print("No withdrawal records found.")
        print("Creating a test withdrawal record...")
        
        # Create a test withdrawal
        cursor.execute('''
            INSERT INTO withdrawal (user_id, amount, fee, net_amount, bank_name, account_number, account_name, status, created_at)
            VALUES (1, 10000.0, 100.0, 9900.0, 'Test Bank', '1234567890', 'Test User', 'pending', datetime('now'))
        ''')
        conn.commit()
        print("Test withdrawal record created!")
        
except Exception as e:
    print(f"Error: {e}")

# Check user table for withdrawal_balance column
print("\nChecking user table structure...")
cursor.execute('PRAGMA table_info(user)')
columns = cursor.fetchall()
withdrawal_balance_exists = any(col[1] == 'withdrawal_balance' for col in columns)
print(f"withdrawal_balance column exists: {withdrawal_balance_exists}")

if not withdrawal_balance_exists:
    print("Adding withdrawal_balance column...")
    try:
        cursor.execute('ALTER TABLE user ADD COLUMN withdrawal_balance FLOAT DEFAULT 0.0')
        conn.commit()
        print("Column added successfully!")
    except Exception as e:
        print(f"Error adding column: {e}")

conn.close()
print("Done!")
