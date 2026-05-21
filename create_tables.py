from app import app, db, User, Package, Transaction, UserPackage, Withdrawal

with app.app_context():
    # Drop all tables first
    db.drop_all()
    print("Dropped all tables")
    
    # Create all tables
    db.create_all()
    print("Created all tables")
    
    # Check what tables were created
    import sqlite3
    conn = sqlite3.connect('fintech.db')
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f'Found {len(tables)} tables:')
    for t in tables:
        print(f'  - {t[0]}')
    conn.close()
