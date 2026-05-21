import sqlite3
import os

def create_database_tables():
    """Create all required database tables using direct SQL"""
    
    # Connect to database
    db_path = 'fintech.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    try:
        # Create user table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(200) NOT NULL,
                phone VARCHAR(20),
                referral_code VARCHAR(20) UNIQUE NOT NULL,
                referred_by INTEGER,
                recharge_balance FLOAT DEFAULT 0.0,
                main_balance FLOAT DEFAULT 0.0,
                total_earned FLOAT DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                is_admin BOOLEAN DEFAULT 0,
                bank_name VARCHAR(100),
                account_number VARCHAR(20),
                account_name VARCHAR(100),
                last_checkin TIMESTAMP,
                FOREIGN KEY (referred_by) REFERENCES user (id)
            )
        ''')
        print("✅ User table created")
        
        # Create package table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS package (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price FLOAT NOT NULL,
                daily_return_rate FLOAT NOT NULL,
                duration_days INTEGER NOT NULL,
                min_recharge FLOAT DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Package table created")
        
        # Create transaction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "transaction" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type VARCHAR(50) NOT NULL,
                amount FLOAT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        print("✅ Transaction table created")
        
        # Create user_package table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_package (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                package_id INTEGER NOT NULL,
                amount_invested FLOAT NOT NULL,
                daily_return FLOAT NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                total_earned FLOAT DEFAULT 0.0,
                last_income_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (package_id) REFERENCES package (id)
            )
        ''')
        print("✅ UserPackage table created")
        
        # Create withdrawal table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS withdrawal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount FLOAT NOT NULL,
                fee FLOAT DEFAULT 0.0,
                net_amount FLOAT NOT NULL,
                bank_name VARCHAR(100),
                account_number VARCHAR(20),
                account_name VARCHAR(100),
                status VARCHAR(20) DEFAULT 'pending',
                admin_note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        print("✅ Withdrawal table created")
        
        # Insert sample packages
        cursor.execute('SELECT COUNT(*) FROM package')
        if cursor.fetchone()[0] == 0:
            packages = [
                ('Starter Package', 'Perfect for beginners - Start your investment journey', 5000.0, 2.86, 30, 0.0, 1),
                ('Silver Package', 'For growing investors - Build your wealth steadily', 25000.0, 2.86, 30, 0.0, 1),
                ('Gold Package', 'Premium investment option - Maximize your returns', 100000.0, 2.86, 30, 0.0, 1),
                ('Platinum Package', 'Ultimate investment package - For serious investors', 500000.0, 2.86, 30, 0.0, 1)
            ]
            
            cursor.executemany('''
                INSERT INTO package (name, description, price, daily_return_rate, duration_days, min_recharge, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', packages)
            print("✅ Sample packages inserted")
        
        # Insert admin user if doesn't exist
        cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', ('admin@fintech.com',))
        if cursor.fetchone()[0] == 0:
            from werkzeug.security import generate_password_hash
            admin_password = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO user (name, email, password_hash, phone, referral_code, main_balance, recharge_balance, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Admin User', 'admin@fintech.com', admin_password, '+2347012345678', 'ADMIN001', 1000000.0, 500000.0, 1))
            print("✅ Admin user created: admin@fintech.com / admin123")
        
        # Insert test user if doesn't exist
        cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', ('test@example.com',))
        if cursor.fetchone()[0] == 0:
            from werkzeug.security import generate_password_hash
            test_password = generate_password_hash('test123')
            cursor.execute('''
                INSERT INTO user (name, email, password_hash, phone, referral_code, main_balance, recharge_balance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('Test User', 'test@example.com', test_password, '+2347098765432', 'TEST0001', 50000.0, 25000.0))
            print("✅ Test user created: test@example.com / test123")
        
        conn.commit()
        
        # Verify tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\n📊 Database tables:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   {table[0]}: {count} records")
        
        print("\n🎉 Database setup complete!")
        print("🔑 Login credentials:")
        print("   Admin: admin@fintech.com / admin123")
        print("   Test User: test@example.com / test123")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    create_database_tables()
