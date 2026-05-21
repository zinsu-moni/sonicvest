"""
Test admin login to diagnose issues
"""

from app import app, db
from admin_routes import init_admin_routes
from admin_db import execute_one, set_db
from werkzeug.security import check_password_hash

# Initialize admin routes
init_admin_routes(db, app)
set_db(db)

with app.app_context():
    print("=" * 60)
    print("🔍 TESTING ADMIN LOGIN")
    print("=" * 60)
    
    # Test 1: Check if admin_db is initialized
    print("\n1. Testing admin_db connection...")
    try:
        from admin_db import db as admin_db_obj
        if admin_db_obj is None:
            print("   ❌ admin_db.db is None - not initialized!")
        else:
            print("   ✅ admin_db.db is initialized")
    except:
        print("   ⚠️  Could not check admin_db.db")
    
    # Test 2: Try execute_one function
    print("\n2. Testing execute_one function...")
    try:
        test_sql = 'SELECT * FROM admin_users WHERE username = :username AND is_active = true'
        admin = execute_one(test_sql, {'username': 'admin'})
        
        if admin:
            print("   ✅ execute_one returned data")
            print(f"   Admin found: {admin.get('username')}")
            print(f"   Email: {admin.get('email')}")
            print(f"   Has password_hash: {bool(admin.get('password_hash'))}")
        else:
            print("   ❌ execute_one returned None")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Test password check
    print("\n3. Testing password verification...")
    try:
        if admin:
            password_hash = admin.get('password_hash')
            test_password = 'admin123'
            matches = check_password_hash(password_hash, test_password)
            print(f"   Password 'admin123' matches: {matches}")
            if matches:
                print("   ✅ Password verification works!")
            else:
                print("   ❌ Password does not match!")
        else:
            print("   ⚠️  No admin user to test")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Direct SQLAlchemy query
    print("\n4. Testing direct SQLAlchemy query...")
    try:
        from sqlalchemy import text
        result = db.session.execute(
            text('SELECT * FROM admin_users WHERE username = :username'),
            {'username': 'admin'}
        ).fetchone()
        
        if result:
            print("   ✅ Direct query successful")
            print(f"   Username: {result.username}")
            password_check = check_password_hash(result.password_hash, 'admin123')
            print(f"   Password matches: {password_check}")
        else:
            print("   ❌ No admin found with direct query")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSIS COMPLETE")
    print("=" * 60)
    print("\nIf all tests passed, admin login should work.")
    print("Try accessing: http://localhost:5000/admin")
    print("Login: admin / admin123")
    print()
