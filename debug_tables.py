import sys
import traceback

try:
    print("Starting table creation...")
    
    print("Importing app components...")
    from app import app, db
    print("✅ app and db imported")
    
    print("Importing models...")
    from app import User, Package, Transaction, UserPackage, Withdrawal
    print("✅ Models imported")
    
    print("Starting app context...")
    with app.app_context():
        print("✅ App context started")
        
        print("Dropping existing tables...")
        db.drop_all()
        print("✅ Tables dropped")
        
        print("Creating new tables...")
        db.create_all()
        print("✅ Tables created")
        
        # Check what tables were created
        print("Checking created tables...")
        import sqlite3
        conn = sqlite3.connect('fintech.db')
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f'Found {len(tables)} tables:')
        for t in tables:
            print(f'  - {t[0]}')
        conn.close()
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Traceback:")
    traceback.print_exc()
