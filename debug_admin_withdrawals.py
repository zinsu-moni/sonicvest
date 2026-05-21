import sqlite3
import os

# Test the exact query used in admin routes
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'fintech.db')
print(f'Database path: {DATABASE_PATH}')
print(f'Database exists: {os.path.exists(DATABASE_PATH)}')

try:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    
    # Test the exact query from admin routes
    withdrawals_list = conn.execute('''
        SELECT t.*, u.name as username, u.email, u.bank_name, u.account_number
        FROM transactions t
        JOIN user u ON t.user_id = u.id
        WHERE t.type = 'withdrawal'
        ORDER BY t.created_at DESC
    ''').fetchall()
    
    print(f'Query returned {len(withdrawals_list)} withdrawals')
    for w in withdrawals_list:
        print(f'  ID: {w["id"]}, User: {w["username"]}, Amount: {w["amount"]}, Status: {w["status"]}')
    
    # Also check if admin routes are working by importing them
    print('\nTesting admin routes import...')
    from admin_routes import admin_bp
    print(f'Admin blueprint registered: {admin_bp is not None}')
    
    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
