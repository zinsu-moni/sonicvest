import sqlite3
from datetime import datetime

print("Creating test withdrawal request...")

try:
    conn = sqlite3.connect('instance/fintech.db')
    cursor = conn.cursor()
    
    # Check if there are any users
    cursor.execute('SELECT id, name, email FROM user LIMIT 1')
    user = cursor.fetchone()
    
    if user:
        print(f"Found user: {user[1]} ({user[2]})")
        
        # Create a test withdrawal
        cursor.execute('''
            INSERT INTO withdrawal (user_id, amount, fee, net_amount, bank_name, account_number, account_name, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user[0], 10000.0, 500.0, 9500.0, 'GTBank', '0123456789', 'Test User', 'pending', datetime.now().isoformat()))
        
        conn.commit()
        print("✅ Test withdrawal request created successfully!")
        
        # Check if it was created
        cursor.execute('SELECT COUNT(*) FROM withdrawal WHERE status = "pending"')
        pending_count = cursor.fetchone()[0]
        print(f"📊 Total pending withdrawals: {pending_count}")
        
    else:
        print("❌ No users found in database")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
