"""
Template test to verify Jinja2 variables
"""

from app import app

def test_templates():
    print("🧪 Testing Template Rendering...")
    
    routes_to_test = [
        ('/', 'Home Page'),
        ('/register', 'Registration Page'),
        ('/login', 'Login Page'),
        ('/packages', 'Packages Page'),
    ]
    
    with app.test_client() as client:
        for route, name in routes_to_test:
            try:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"✅ {name}: OK (Status {response.status_code})")
                else:
                    print(f"⚠️  {name}: Status {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: Error - {str(e)}")
    
    print("\n🎉 Template testing complete!")

if __name__ == '__main__':
    test_templates()
