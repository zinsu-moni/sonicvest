import sqlite3
from werkzeug.security import generate_password_hash

def add_sample_data():
    """Add sample data to existing database tables"""
    
    conn = sqlite3.connect('fintech.db')
    cursor = conn.cursor()
    
    try:
        # Insert sample packages
        cursor.execute('SELECT COUNT(*) FROM package')
        if cursor.fetchone()[0] == 0:
            packages = [
                ('Starter Package', 'Perfect for beginners - Start your investment journey', 5000.0, 2.86, 30, 1),
                ('Silver Package', 'For growing investors - Build your wealth steadily', 25000.0, 2.86, 30, 1),
                ('Gold Package', 'Premium investment option - Maximize your returns', 100000.0, 2.86, 30, 1),
                ('Platinum Package', 'Ultimate investment package - For serious investors', 500000.0, 2.86, 30, 1)
            ]
            
            cursor.executemany('''
                INSERT INTO package (name, description, price, daily_return_rate, duration_days, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', packages)
            print("✅ Sample packages inserted")
        
        # Insert admin user if doesn't exist
        cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', ('admin@fintech.com',))
        if cursor.fetchone()[0] == 0:
            admin_password = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO user (name, email, password_hash, phone, referral_code, main_balance, recharge_balance, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Admin User', 'admin@fintech.com', admin_password, '+2347012345678', 'ADMIN001', 1000000.0, 500000.0, 1))
            print("✅ Admin user created: admin@fintech.com / admin123")
        
        # Insert test user if doesn't exist
        cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', ('test@example.com',))
        if cursor.fetchone()[0] == 0:
            test_password = generate_password_hash('test123')
            cursor.execute('''
                INSERT INTO user (name, email, password_hash, phone, referral_code, main_balance, recharge_balance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('Test User', 'test@example.com', test_password, '+2347098765432', 'TEST0001', 50000.0, 25000.0))
            print("✅ Test user created: test@example.com / test123")
        
        conn.commit()
        
        # Show final counts
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM package")
        package_count = cursor.fetchone()[0]
        
        print(f"\n📊 Final counts:")
        print(f"   Users: {user_count}")
        print(f"   Packages: {package_count}")
        
        print("\n🎉 Sample data added successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_sample_data()
