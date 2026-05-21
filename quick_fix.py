import sqlite3
import os

# Check both possible database locations
db_paths = ['fintech.db', 'instance/fintech.db']

for db_path in db_paths:
    if os.path.exists(db_path):
        print(f'Found database at: {db_path}')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add missing columns
        try:
            cursor.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0')
            print('✓ Added is_admin column')
        except Exception as e:
            print(f'✓ is_admin column already exists ({str(e)[:50]}...)')
        
        try:
            cursor.execute('ALTER TABLE user ADD COLUMN bank_name VARCHAR(100)')
            print('✓ Added bank_name column')
        except Exception as e:
            print(f'✓ bank_name column already exists ({str(e)[:50]}...)')
        
        try:
            cursor.execute('ALTER TABLE user ADD COLUMN account_number VARCHAR(50)')
            print('✓ Added account_number column')
        except Exception as e:
            print(f'✓ account_number column already exists ({str(e)[:50]}...)')
        
        try:
            cursor.execute('ALTER TABLE user ADD COLUMN account_name VARCHAR(100)')
            print('✓ Added account_name column')
        except Exception as e:
            print(f'✓ account_name column already exists ({str(e)[:50]}...)')
        
        conn.commit()
        conn.close()
        print(f'🎉 Database migration completed for {db_path}!')
    else:
        print(f'❌ Database not found at {db_path}')

print('\n✅ Migration script completed!')
