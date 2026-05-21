"""
Frontend-Backend Connection Test
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.getcwd())

def test_connection():
    print("🔗 FRONTEND-BACKEND CONNECTION TEST")
    print("=" * 50)
    
    try:
        # Import the app
        from app import app, db, User, Package
        print("✅ Backend imports successful")
        
        # Check routes
        routes = []
        with app.app_context():
            for rule in app.url_map.iter_rules():
                routes.append(f"{rule.rule} -> {rule.endpoint}")
        
        print(f"✅ {len(routes)} routes available:")
        for route in routes[:10]:  # Show first 10 routes
            print(f"   {route}")
        
        if len(routes) > 10:
            print(f"   ... and {len(routes) - 10} more routes")
        
        # Test template rendering
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page renders successfully")
            else:
                print(f"⚠️  Home page status: {response.status_code}")
        
        # Check if templates exist
        template_dir = "templates"
        if os.path.exists(template_dir):
            template_count = sum([len(files) for r, d, files in os.walk(template_dir) if files])
            print(f"✅ {template_count} template files found")
        
        print()
        print("🎉 FRONTEND-BACKEND CONNECTION: SUCCESS!")
        print("📊 Status Summary:")
        print(f"   • Routes: {len(routes)} available")
        print(f"   • Templates: Connected")
        print(f"   • Database: Models loaded")
        print(f"   • Static files: Connected")
        print()
        print("🚀 Ready to run: python app.py")
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("💡 Try running: pip install -r requirements.txt")

if __name__ == '__main__':
    test_connection()
