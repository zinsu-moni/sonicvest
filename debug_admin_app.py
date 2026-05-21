#!/usr/bin/env python3
"""
Debug version of the main app
"""
import os
import sys

print("🚀 Starting debug version...")
print("📂 Current directory:", os.getcwd())
print("🐍 Python version:", sys.version)

try:
    print("Step 1: Importing Flask...")
    from flask import Flask
    print("✅ Flask imported successfully")
    
    print("Step 2: Creating Flask app...")
    app = Flask(__name__)
    app.secret_key = 'debug-secret-key'
    print("✅ Flask app created")
    
    print("Step 3: Importing admin routes...")
    from admin_routes import admin_bp
    print("✅ Admin routes imported")
    
    print("Step 4: Registering admin blueprint...")
    app.register_blueprint(admin_bp)
    print("✅ Admin blueprint registered")
    
    print("Step 5: Adding test route...")
    @app.route('/')
    def home():
        return '''
        <h1>🎉 Main App Debug - Working!</h1>
        <p><a href="/admin">Go to Admin Panel</a></p>
        <p><a href="/admin/login">Admin Login</a></p>
        <p><a href="/admin/dashboard">Admin Dashboard</a></p>
        '''
    print("✅ Test route added")
    
    print("Step 6: Starting server...")
    app.run(debug=True, host='0.0.0.0', port=5001)
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ General Error: {e}")
    import traceback
    traceback.print_exc()
