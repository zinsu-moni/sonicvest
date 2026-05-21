#!/usr/bin/env python3

"""
Create a test deposit transaction for receipt testing
"""

from app import app, db, User, Transaction
from datetime import datetime
import secrets

def create_test_transaction():
    with app.app_context():
        print("=== Creating Test Deposit Transaction ===")
        
        # Find a test user
        user = User.query.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return
            
        # Generate a unique reference
        timestamp = datetime.now().strftime("%m%d%H%M")
        reference = f"GTR{timestamp}{secrets.token_urlsafe(4)[:4].upper()}"
        
        # Create a test transaction
        test_transaction = Transaction(
            user_id=user.id,
            type='deposit',
            amount=5000.0,
            description='Test Deposit via GTR Pay - Receipt System Test',
            status='completed',
            reference=reference,
            created_at=datetime.now()
        )
        
        db.session.add(test_transaction)
        db.session.commit()
        
        print(f"✅ Test transaction created successfully!")
        print(f"📋 Transaction ID: {test_transaction.id}")
        print(f"🔖 Reference: {reference}")
        print(f"💰 Amount: ₦{test_transaction.amount:,.2f}")
        print(f"👤 User: {user.username} ({user.email})")
        print(f"📄 Receipt URL: http://localhost:5000/deposit/receipt/{reference}")
        print("\n🚀 Start your Flask app and visit the receipt URL to test!")

if __name__ == '__main__':
    create_test_transaction()
