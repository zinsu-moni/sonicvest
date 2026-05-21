"""
Simple database setup script
"""

import os
import sqlite3

def setup_database():
    print("🗄️  Setting up database...")
    
    # Create instance directory
    instance_dir = os.path.join(os.getcwd(), 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    print(f"✅ Instance directory created: {instance_dir}")
    
    # Create database file
    db_path = os.path.join(instance_dir, 'fintech.db')
    
    try:
        # Test SQLite connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create a simple test table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database created successfully: {db_path}")
        print(f"✅ Database file size: {os.path.getsize(db_path)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

if __name__ == '__main__':
    setup_database()
