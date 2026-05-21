"""
Initialize PostgreSQL database with all required tables.
Run this script after switching to PostgreSQL.
"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify DATABASE_URL is set and is PostgreSQL
database_url = os.environ.get('DATABASE_URL', '')
if not database_url.startswith('postgresql://') and not database_url.startswith('postgres://'):
    print("❌ ERROR: DATABASE_URL is not set to PostgreSQL!")
    print(f"Current DATABASE_URL: {database_url}")
    print("\nPlease set DATABASE_URL in your .env file to a PostgreSQL connection string.")
    print("Example: postgresql://user:password@host:port/database")
    exit(1)

print(f"✅ PostgreSQL database configured: {database_url[:30]}...")

# Import app and db after environment is loaded
from app import app, db

def init_postgres_db():
    """Initialize PostgreSQL database with all tables."""
    with app.app_context():
        try:
            print("\n🔄 Creating all database tables...")
            
            # Drop all tables first (use with caution!)
            print("⚠️  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("📋 Creating new tables...")
            db.create_all()
            
            print("✅ Database tables created successfully!")
            
            # Verify tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📊 Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"   - {table}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("PostgreSQL Database Initialization")
    print("=" * 60)
    
    response = input("\n⚠️  This will DROP all existing tables and recreate them.\nType 'YES' to continue: ")
    
    if response.strip().upper() == 'YES':
        success = init_postgres_db()
        if success:
            print("\n✅ PostgreSQL database is ready to use!")
            print("\nNext steps:")
            print("1. Create an admin user using: python create_admin_user.py")
            print("2. Run the app with: python app.py")
        else:
            print("\n❌ Database initialization failed. Please check the errors above.")
    else:
        print("\n❌ Operation cancelled.")
