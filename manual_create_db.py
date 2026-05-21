import sqlite3

# Create all tables manually
conn = sqlite3.connect('fintech.db')
cursor = conn.cursor()

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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    is_admin BOOLEAN DEFAULT 0,
    bank_name VARCHAR(100),
    account_number VARCHAR(20),
    account_name VARCHAR(100),
    last_checkin DATETIME,
    FOREIGN KEY (referred_by) REFERENCES user (id)
)
''')

# Create package table
cursor.execute('''
CREATE TABLE IF NOT EXISTS package (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    daily_return_rate FLOAT NOT NULL,
    duration_days INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Create transaction table
cursor.execute('''
CREATE TABLE IF NOT EXISTS "transaction" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

# Create user_package table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_package (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    purchase_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    total_earnings FLOAT DEFAULT 0.0,
    last_income_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (package_id) REFERENCES package (id)
)
''')

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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

conn.commit()

# Check created tables
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f'Successfully created {len(tables)} tables:')
for t in tables:
    print(f'  - {t[0]}')

conn.close()
print("✅ Database tables created successfully!")
