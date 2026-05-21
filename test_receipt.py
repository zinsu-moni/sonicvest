#!/usr/bin/env python3

"""
Test the receipt system by creating a sample transaction and viewing the receipt
"""

from app import app, db, User, Transaction
from datetime import datetime

def test_receipt():
    with app.app_context():
        print("=== Testing Receipt System ===")
        
        # Find a test user
        user = User.query.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return
            
        # Create a test transaction
        test_transaction = Transaction(
            user_id=user.id,
            type='deposit',
            amount=5000.0,
            description='Test Deposit via GTR Pay',
            status='completed',
            reference='GTR08131425TEST',
            created_at=datetime.now()
        )
        
        db.session.add(test_transaction)
        db.session.commit()
        
        print(f"✅ Test transaction created: {test_transaction.reference}")
        print(f"📄 Receipt URL: /deposit/receipt/{test_transaction.reference}")
        print(f"🌐 Full URL: http://localhost:5000/deposit/receipt/{test_transaction.reference}")
        
        # Start the app
        print("\n🚀 Starting Flask app...")
        print("Navigate to the receipt URL above to test the receipt display")
        app.run(debug=True, port=5000)

if __name__ == '__main__':
    test_receipt()
