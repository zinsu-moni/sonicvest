"""
Production database initialization script
Run this before starting the application in production
"""

import os
import sys

def init_production_database():
    """Initialize database for production deployment"""
    print("🗄️  Initializing production database...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Create all tables if they don't exist
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Initialize admin database
            try:
                from admin_routes import init_admin_db
                init_admin_db()
                print("✅ Admin database initialized")
            except Exception as e:
                print(f"⚠️  Admin initialization: {e}")
            
            # Migration: Add missing columns to existing database
            try:
                import sqlite3
                db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fintech.db')
                
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Check if user table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
                    if cursor.fetchone():
                        cursor.execute("PRAGMA table_info(user)")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        # Add missing columns
                        migrations = [
                            ('is_admin', 'BOOLEAN DEFAULT 0'),
                            ('bank_name', 'VARCHAR(100)'),
                            ('account_number', 'VARCHAR(50)'),
                            ('account_name', 'VARCHAR(100)'),
                            ('last_checkin', 'DATETIME')
                        ]
                        
                        for col_name, col_type in migrations:
                            if col_name not in columns:
                                try:
                                    cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} {col_type}")
                                    print(f"✅ Added column: {col_name}")
                                except Exception as col_error:
                                    print(f"⚠️  Column {col_name}: {col_error}")
                        
                        conn.commit()
                    conn.close()
                    print("✅ Database migration completed")
            except Exception as migration_error:
                print(f"⚠️  Migration: {migration_error}")

            # Normalize production defaults so hosted deployments use the same check-in bonus as local
            try:
                from app import execute_update

                updated_rows = execute_update(
                    'UPDATE system_settings SET daily_checkin_bonus = :bonus WHERE daily_checkin_bonus = 20 OR daily_checkin_bonus IS NULL',
                    {'bonus': 100.0}
                )
                if updated_rows:
                    print('✅ Daily check-in bonus normalized to ₦100')
            except Exception as bonus_error:
                print(f"⚠️  Bonus normalization: {bonus_error}")
            
            print("✅ Production database ready!")
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_production_database()
    sys.exit(0 if success else 1)
