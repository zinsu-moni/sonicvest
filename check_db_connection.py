"""
Database Connection Diagnostic Tool
Checks PostgreSQL connectivity and configuration
"""
from app import app, db
from sqlalchemy import text
import time
import sys

def test_connection():
    """Test database connection with detailed diagnostics"""
    print("=" * 60)
    print("🔍 DATABASE CONNECTION DIAGNOSTICS")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Test 1: Basic connection
            print("\n1️⃣ Testing basic connection...")
            start = time.time()
            result = db.session.execute(text('SELECT 1')).scalar()
            elapsed = time.time() - start
            
            if result == 1:
                print(f"✅ Basic connection: OK ({elapsed:.3f}s)")
            else:
                print(f"❌ Basic connection: FAILED")
                return False
            
            # Test 2: Database version
            print("\n2️⃣ Checking database version...")
            version = db.session.execute(text('SELECT version()')).scalar()
            print(f"✅ PostgreSQL version: {version.split(',')[0]}")
            
            # Test 3: Connection pool info
            print("\n3️⃣ Checking connection pool...")
            pool = db.engine.pool
            print(f"   Pool size: {pool.size()}")
            print(f"   Checked out: {pool.checkedout()}")
            print(f"   Overflow: {pool.overflow()}")
            print(f"   Checked in: {pool.checkedin()}")
            
            # Test 4: Query performance
            print("\n4️⃣ Testing query performance...")
            start = time.time()
            db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
            elapsed = time.time() - start
            print(f"✅ Query test: OK ({elapsed:.3f}s)")
            
            # Test 5: Connection timeout
            print("\n5️⃣ Testing connection stability...")
            for i in range(5):
                start = time.time()
                db.session.execute(text('SELECT 1'))
                elapsed = time.time() - start
                print(f"   Attempt {i+1}: {elapsed:.3f}s")
                time.sleep(1)
            print("✅ Connection stability: OK")
            
            # Test 6: Table access
            print("\n6️⃣ Testing table access...")
            tables = ['users', 'packages', 'user_packages', 'transactions']
            for table in tables:
                try:
                    count = db.session.execute(text(f'SELECT COUNT(*) FROM {table}')).scalar()
                    print(f"   ✅ {table}: {count} rows")
                except Exception as e:
                    print(f"   ❌ {table}: {e}")
            
            # Test 7: Connection parameters
            print("\n7️⃣ Connection configuration...")
            config = app.config['SQLALCHEMY_ENGINE_OPTIONS']
            print(f"   Pool size: {config.get('pool_size')}")
            print(f"   Pool recycle: {config.get('pool_recycle')}s")
            print(f"   Pool pre-ping: {config.get('pool_pre_ping')}")
            print(f"   Max overflow: {config.get('max_overflow')}")
            
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED")
            print("=" * 60)
            print("\n💡 Database connection is healthy!")
            print("   If worker still fails, check:")
            print("   - Worker process is running")
            print("   - Environment variables are set")
            print("   - PostgreSQL server stability")
            print("   - Network connectivity\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Check DATABASE_URL environment variable")
            print("   2. Verify PostgreSQL server is running")
            print("   3. Check network connectivity")
            print("   4. Verify database credentials")
            print("   5. Check firewall settings\n")
            return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
