#!/usr/bin/env python3
"""
Add sample withdrawal records to the database for testing.
"""

from app import app, db, User, Transaction
from datetime import datetime, timedelta
import random

def add_sample_withdrawals():
    """Add sample withdrawal transactions for the demo user"""
    
    with app.app_context():
        # Find the demo user
        user = User.query.filter_by(email='demo@fintech.com').first()
        
        if not user:
            print("❌ Demo user not found. Please run reset_database.py first.")
            return
        
        print(f"👤 Adding sample withdrawals for: {user.name}")
        
        # Sample withdrawal data
        sample_withdrawals = [
            {
                'amount': 5000.0,
                'status': 'completed',
                'description': 'Bank transfer withdrawal',
                'days_ago': 15
            },
            {
                'amount': 2500.0,
                'status': 'completed',
                'description': 'Emergency withdrawal',
                'days_ago': 8
            },
            {
                'amount': 7500.0,
                'status': 'pending',
                'description': 'Monthly withdrawal',
                'days_ago': 2
            },
            {
                'amount': 3000.0,
                'status': 'completed',
                'description': 'Profit withdrawal',
                'days_ago': 25
            },
            {
                'amount': 1500.0,
                'status': 'failed',
                'description': 'Insufficient balance',
                'days_ago': 5
            }
        ]
        
        # Create withdrawal transactions
        for withdrawal_data in sample_withdrawals:
            # Calculate the date
            created_date = datetime.utcnow() - timedelta(days=withdrawal_data['days_ago'])
            
            # Generate reference ID
            reference = f"WD{random.randint(100000, 999999)}"
            
            withdrawal = Transaction(
                user_id=user.id,
                type='withdrawal',
                amount=withdrawal_data['amount'],
                description=withdrawal_data['description'],
                status=withdrawal_data['status'],
                reference=reference,
                created_at=created_date
            )
            
            db.session.add(withdrawal)
            print(f"   ✅ Added withdrawal: ₦{withdrawal_data['amount']:,.0f} ({withdrawal_data['status']})")
        
        # Commit all transactions
        db.session.commit()
        
        # Show summary
        total_withdrawals = Transaction.query.filter_by(user_id=user.id, type='withdrawal').count()
        completed_withdrawals = Transaction.query.filter_by(user_id=user.id, type='withdrawal', status='completed').count()
        
        print(f"\n📊 Summary:")
        print(f"   Total withdrawals: {total_withdrawals}")
        print(f"   Completed: {completed_withdrawals}")
        print(f"   User: {user.name} ({user.email})")
        print("\n🎉 Sample withdrawal data added successfully!")
        print("💡 You can now test the withdrawal history page")

if __name__ == '__main__':
    add_sample_withdrawals()
