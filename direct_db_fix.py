import os
import sqlite3

# Direct database operation without importing app
db_path = os.path.join('instance', 'fintech.db')
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current table structure
    cursor.execute("PRAGMA table_info(user)")
    columns = cursor.fetchall()
    print("\nCurrent user table columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Check if is_admin column exists
    column_names = [col[1] for col in columns]
    
    if 'is_admin' not in column_names:
        print("\n🔧 Adding is_admin column...")
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            conn.commit()
            print("✅ Successfully added is_admin column")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("\n✅ is_admin column already exists")
    
    # Check if bank columns exist
    bank_columns = ['bank_name', 'account_number', 'account_name']
    for col_name in bank_columns:
        if col_name not in column_names:
            print(f"\n🔧 Adding {col_name} column...")
            try:
                if col_name == 'bank_name':
                    cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} VARCHAR(100)")
                elif col_name == 'account_number':
                    cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} VARCHAR(50)")
                elif col_name == 'account_name':
                    cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} VARCHAR(100)")
                conn.commit()
                print(f"✅ Successfully added {col_name} column")
            except Exception as e:
                print(f"❌ Error adding {col_name}: {e}")
        else:
            print(f"✅ {col_name} column already exists")
    
    conn.close()
    print("\n🎉 Database migration completed!")
else:
    print("❌ Database file not found!")
