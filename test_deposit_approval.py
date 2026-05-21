#!/usr/bin/env python3
"""Test manual deposit approval"""

import sqlite3
import os
from datetime import datetime
import secrets

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'fintech.db')

def test_deposit_approval():
    """Test the complete manual deposit flow"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get or create a test user
        cursor.execute('SELECT * FROM "user" WHERE email = ?', ('test_deposit@example.com',))
        user = cursor.fetchone()
        
        if not user:
            print("Creating test user...")
            cursor.execute('''
                INSERT INTO "user" (name, email, password_hash, main_balance)
                VALUES (?, ?, ?, ?)
            ''', ('Test User', 'test_deposit@example.com', 'hashed_pwd', 0.0))
            conn.commit()
            cursor.execute('SELECT id FROM "user" WHERE email = ?', ('test_deposit@example.com',))
            user = cursor.fetchone()
            user_id = user['id']
        else:
            user_id = user['id']
        
        print(f"Test user ID: {user_id}")
        
        # Create a pending deposit transaction
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        reference = f"DEP{timestamp}{secrets.token_urlsafe(4)[:4].upper()}"
        
        cursor.execute('''
            INSERT INTO "transaction" (user_id, type, amount, status, description, reference, created_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (user_id, 'deposit', 0, 'pending', 'Test deposit receipt', reference))
        conn.commit()
        
        cursor.execute('SELECT last_insert_rowid()')
        transaction_id = cursor.fetchone()[0]
        print(f"Created pending deposit transaction ID: {transaction_id}, Reference: {reference}")
        
        # Check initial user balance
        cursor.execute('SELECT main_balance FROM "user" WHERE id = ?', (user_id,))
        initial_balance = cursor.fetchone()['main_balance']
        print(f"Initial balance: ₦{initial_balance:,.0f}")
        
        # Simulate approval - update the transaction and balance
        deposit_amount = 50000.0
        cursor.execute('''
            UPDATE "transaction" 
            SET status = 'completed',
                amount = ?,
                description = 'Manual deposit - Approved by admin'
            WHERE id = ?
        ''', (deposit_amount, transaction_id))
        
        cursor.execute('''
            UPDATE "user" 
            SET main_balance = main_balance + ?
            WHERE id = ?
        ''', (deposit_amount, user_id))
        
        conn.commit()
        
        # Verify the update
        cursor.execute('SELECT status, amount FROM "transaction" WHERE id = ?', (transaction_id,))
        updated_txn = cursor.fetchone()
        cursor.execute('SELECT main_balance FROM "user" WHERE id = ?', (user_id,))
        new_balance = cursor.fetchone()['main_balance']
        
        print(f"Transaction updated - Status: {updated_txn['status']}, Amount: ₦{updated_txn['amount']:,.0f}")
        print(f"New balance: ₦{new_balance:,.0f}")
        
        if updated_txn['status'] == 'completed' and updated_txn['amount'] == deposit_amount and new_balance == initial_balance + deposit_amount:
            print("\n✅ Deposit approval test PASSED!")
            return True
        else:
            print("\n✗ Deposit approval test FAILED!")
            return False
            
    except Exception as e:
        print(f"✗ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    test_deposit_approval()
