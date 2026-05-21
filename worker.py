"""
Background Worker for Income Distribution
This file runs as a separate process to handle automated income payouts
"""
from app import app, db, User, UserPackage, Transaction, SYSTEM_SETTINGS
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError
import time
import os

def distribute_income():
    """Process income distribution for all active packages"""
    with app.app_context():
        try:
            # Test database connection first
            try:
                db.session.execute(text('SELECT 1'))
                db.session.commit()
            except Exception as e:
                print(f"⚠️  Database connection test failed: {e}")
                db.session.rollback()
                # Try to reconnect
                db.session.remove()
                db.engine.dispose()
                time.sleep(2)
                return 0
            
            current_time = datetime.now(timezone.utc)
            processed = 0
            
            # Get all active user packages
            active_packages = UserPackage.query.filter(
                UserPackage.is_active == True,
                UserPackage.end_date > current_time
            ).all()
            
            for user_package in active_packages:
                # Check if enough time has passed since last payout
                hours_since_last_payout = SYSTEM_SETTINGS['INCOME_DROP_HOURS']
                
                # Convert naive datetimes to UTC aware if needed
                start_date = user_package.start_date.replace(tzinfo=timezone.utc) if user_package.start_date.tzinfo is None else user_package.start_date
                last_payout = user_package.last_payout.replace(tzinfo=timezone.utc) if user_package.last_payout and user_package.last_payout.tzinfo is None else user_package.last_payout
                
                if last_payout is None:
                    # First payout - check if package started more than specified hours ago
                    time_since_start = current_time - start_date
                    if time_since_start.total_seconds() >= hours_since_last_payout * 3600:
                        should_payout = True
                    else:
                        should_payout = False
                else:
                    # Check time since last payout
                    time_since_last = current_time - last_payout
                    should_payout = time_since_last.total_seconds() >= hours_since_last_payout * 3600
                
                if should_payout:
                    # Process the payout
                    user = db.session.get(User, user_package.user_id)
                    if not user:
                        print(f"⚠️  User {user_package.user_id} not found")
                        continue
                    payout_amount = user_package.daily_return
                    
                    # Add to user's main balance
                    user.main_balance += payout_amount
                    user.total_earned += payout_amount
                    
                    # Update package's total earned
                    user_package.total_earned = (user_package.total_earned or 0) + payout_amount
                    
                    # Update last payout time
                    user_package.last_payout = current_time
                    
                    # Create transaction record
                    transaction = Transaction(
                        user_id=user.id,
                        type='package_income',
                        amount=payout_amount,
                        description=f'Income from {user_package.package.name}',
                        status='completed'
                    )
                    
                    db.session.add(transaction)
                    processed += 1
            
            if processed > 0:
                db.session.commit()
                print(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processed {processed} income payouts")
            else:
                print(f"⏳ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No payouts due")
                
            return processed
            
        except (OperationalError, DatabaseError) as e:
            print(f"❌ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Database error: {e}")
            db.session.rollback()
            db.session.remove()
            db.engine.dispose()
            print("🔄 Connection disposed, will retry...")
            return 0
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error distributing income: {e}")
            db.session.rollback()
            return 0

def run_worker():
    """Main worker loop"""
    print("=" * 60)
    print("🚀 INCOME DISTRIBUTION WORKER STARTED")
    print("=" * 60)
    print(f"⏰ Income drops every: {SYSTEM_SETTINGS['INCOME_DROP_HOURS']} hours")
    print(f"🔄 Checking every: 30 seconds")
    print(f"🌐 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    print(f"🔌 Database: Connected")
    print("=" * 60)
    
    check_count = 0
    error_count = 0
    max_errors = 10
    
    while True:
        try:
            check_count += 1
            if check_count % 120 == 0:  # Log heartbeat every hour (120 * 30 seconds)
                print(f"💓 Worker heartbeat - Still running ({check_count} checks completed, {error_count} errors)")
            
            processed = distribute_income()
            
            # Reset error count on successful run
            if processed >= 0:
                error_count = 0
            
            # Sleep for 30 seconds before next check
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n🛑 Worker stopped by user")
            break
        except Exception as e:
            error_count += 1
            print(f"❌ Worker error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                print(f"🚨 Too many errors ({max_errors}), shutting down...")
                break
            
            print("⏳ Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == '__main__':
    run_worker()
