from app import app, db, User, Package, Transaction, UserPackage, Withdrawal

print("🗄️  Starting database initialization...")

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Database tables created")
    
    # Check if withdrawal table exists now
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Available tables: {tables}")
    
    if 'withdrawal' in tables:
        columns = inspector.get_columns('withdrawal')
        print("Withdrawal table columns:")
        for col in columns:
            print(f"  {col['name']} - {col['type']}")
    
print("🎉 Database check complete!")
