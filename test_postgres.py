"""
Test PostgreSQL database connection.
"""

from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Get DATABASE_URL
database_url = os.environ.get('DATABASE_URL', '')

print("=" * 60)
print("PostgreSQL Connection Test")
print("=" * 60)

# Check if DATABASE_URL is set
if not database_url:
    print("❌ DATABASE_URL is not set in .env file!")
    sys.exit(1)

# Check if it's PostgreSQL
if not (database_url.startswith('postgresql://') or database_url.startswith('postgres://')):
    print(f"❌ DATABASE_URL is not PostgreSQL: {database_url}")
    sys.exit(1)

# Mask password for display
try:
    parts = database_url.split('@')
    if len(parts) > 1:
        masked = parts[0].split(':')[0:2]
        masked_url = f"{masked[0]}:***@{parts[1]}"
    else:
        masked_url = database_url[:20] + "..."
    print(f"✅ DATABASE_URL configured: {masked_url}")
except:
    print(f"✅ DATABASE_URL configured: {database_url[:30]}...")

# Test connection
print("\n🔄 Testing database connection...")

try:
    from sqlalchemy import create_engine, text
    
    # Fix postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Create engine
    engine = create_engine(database_url)
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✅ Connection successful!")
        print(f"\n📊 PostgreSQL Version:")
        print(f"   {version[:80]}...")
        
        # Get database info
        result = connection.execute(text("SELECT current_database()"))
        db_name = result.fetchone()[0]
        print(f"\n📁 Database: {db_name}")
        
        # Check if tables exist
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            print(f"\n📋 Existing tables ({len(tables)}):")
            for table in tables:
                print(f"   - {table}")
        else:
            print("\n⚠️  No tables found. Run 'python init_postgres.py' to create tables.")
    
    print("\n✅ PostgreSQL is ready to use!")
    
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Verify your DATABASE_URL in .env file")
    print("2. Check if the database server is running")
    print("3. Verify your database credentials")
    print("4. Check if your IP is whitelisted (for cloud databases)")
    sys.exit(1)
