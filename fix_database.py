import sqlite3
import os

def fix_database():
    """Fix database by adding missing columns"""
    db_path = os.path.join('instance', 'fintech.db')
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add is_admin column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            print("✓ Added is_admin column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✓ is_admin column already exists")
            else:
                print(f"Error adding is_admin: {e}")
        
        # Add bank columns if they don't exist
        for column, column_type in [
            ('bank_name', 'VARCHAR(100)'),
            ('account_number', 'VARCHAR(50)'),
            ('account_name', 'VARCHAR(100)')
        ]:
            try:
                cursor.execute(f"ALTER TABLE user ADD COLUMN {column} {column_type}")
                print(f"✓ Added {column} column")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"✓ {column} column already exists")
                else:
                    print(f"Error adding {column}: {e}")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
