#!/usr/bin/env python3
"""Script to add 100,000 to the first three users"""

from app import app, db, User

def add_balance_to_users():
    with app.app_context():
        # Get first three users
        users = User.query.limit(3).all()
        
        if len(users) == 0:
            print("No users found in database")
            return
            
        print(f"Found {len(users)} users to update")
        
        for i, user in enumerate(users, 1):
            print(f"\nUser {i}:")
            print(f"  Username: {user.username}")
            print(f"  Before - Withdrawal Balance: ₦{user.withdrawal_balance:,.2f}")
            print(f"  Before - Recharge Balance: ₦{user.recharge_balance:,.2f}")
            
            # Add 100,000 to withdrawal balance
            user.add_withdrawal_balance(100000, "Admin bonus - 100K added")
            
            print(f"  After - Withdrawal Balance: ₦{user.withdrawal_balance:,.2f}")
            print(f"  After - Recharge Balance: ₦{user.recharge_balance:,.2f}")
        
        # Commit all changes
        db.session.commit()
        print(f"\n✅ Successfully added ₦100,000 to {len(users)} users!")

if __name__ == "__main__":
    add_balance_to_users()
