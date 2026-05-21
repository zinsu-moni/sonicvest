#!/usr/bin/env python3
"""
Add sample deposit records for testing the deposit history feature.
"""

from app import app, db, User, Transaction
from datetime import datetime, timedelta
import secrets

def add_sample_deposits():
    """Add sample deposit transactions for demo user"""
    
    with app.app_context():
        # Find the demo user
        demo_user = User.query.filter_by(email='demo@fintech.com').first()
        
        if not demo_user:
            print("❌ Demo user not found. Please run reset_database.py first.")
            return
        
        # Check if deposits already exist
        existing_deposits = Transaction.query.filter_by(
            user_id=demo_user.id, 
            type='deposit'
        ).count()
        
        if existing_deposits > 0:
            print(f"✅ Found {existing_deposits} existing deposits for demo user")
            return
        
        print("📝 Adding sample deposit records...")
        
        # Sample deposit data
        deposits = [
            {
                'amount': 10000.0,
                'status': 'completed',
                'description': 'Initial deposit via GTR Bank',
                'days_ago': 15
            },
            {
                'amount': 25000.0,
                'status': 'completed',
                'description': 'Top-up deposit via Bank Transfer',
                'days_ago': 10
            },
            {
                'amount': 5000.0,
                'status': 'completed',
                'description': 'Quick deposit via GTR Pay',
                'days_ago': 7
            },
            {
                'amount': 15000.0,
                'status': 'pending',
                'description': 'Recent deposit via GTR Bank',
                'days_ago': 1
            },
            {
                'amount': 50000.0,
                'status': 'pending',
                'description': 'Large deposit via Bank Transfer',
                'days_ago': 0
            }
        ]
        
        # Create deposit transactions
        for i, deposit_data in enumerate(deposits):
            reference = f"DEP{secrets.token_urlsafe(6)[:6].upper()}"
            created_date = datetime.utcnow() - timedelta(days=deposit_data['days_ago'])
            
            transaction = Transaction(
                user_id=demo_user.id,
                type='deposit',
                amount=deposit_data['amount'],
                description=deposit_data['description'],
                status=deposit_data['status'],
                reference=reference,
                created_at=created_date
            )
            
            db.session.add(transaction)
            print(f"   ✅ Added: ₦{deposit_data['amount']:,.0f} - {deposit_data['status']} - {reference}")
        
        # Update user's balance based on completed deposits
        completed_deposits = [d for d in deposits if d['status'] == 'completed']
        total_completed = sum(d['amount'] for d in completed_deposits)
        
        demo_user.recharge_balance += total_completed
        
        db.session.commit()
        
        print(f"\n✅ Added {len(deposits)} sample deposits")
        print(f"💰 Updated user balance: +₦{total_completed:,.0f} to recharge balance")
        print(f"💰 New recharge balance: ₦{demo_user.recharge_balance:,.0f}")
        print("\n🎯 You can now test the deposit history feature!")

if __name__ == '__main__':
    add_sample_deposits()
