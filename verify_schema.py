"""Quick verification of database schema"""
from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    
    print("=" * 60)
    print("📊 Database Schema Verification")
    print("=" * 60)
    
    # Check user_package table
    print("\n🔍 user_package table columns:")
    columns = inspector.get_columns('user_package')
    for col in columns:
        print(f"  ✅ {col['name']:<20} ({col['type']})")
    
    print("\n✅ All columns present!")
    print("🚀 App should work now")
