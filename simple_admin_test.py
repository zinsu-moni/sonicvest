#!/usr/bin/env python3
"""
Simple admin dashboard test
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'test-secret-key-for-admin'

# Database path
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'fintech.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return '''
    <h1>🚀 Simple Admin Test</h1>
    <p><a href="/admin/login">Go to Admin Login</a></p>
    <p><a href="/admin/dashboard">Go to Admin Dashboard (direct)</a></p>
    <p><a href="/test-db">Test Database Connection</a></p>
    '''

@app.route('/test-db')
def test_db():
    """Test database connection"""
    try:
        conn = get_db_connection()
        
        # Test user table
        users = conn.execute('SELECT COUNT(*) as count FROM user').fetchone()
        user_count = users['count'] if users else 0
        
        # Test package table
        packages = conn.execute('SELECT COUNT(*) as count FROM package').fetchone()
        package_count = packages['count'] if packages else 0
        
        # Test transaction table
        transactions = conn.execute('SELECT COUNT(*) as count FROM "transaction"').fetchone()
        transaction_count = transactions['count'] if transactions else 0
        
        conn.close()
        
        return f'''
        <h1>✅ Database Test Results</h1>
        <ul>
            <li>Users: {user_count}</li>
            <li>Packages: {package_count}</li>
            <li>Transactions: {transaction_count}</li>
        </ul>
        <p><a href="/">Back to Home</a></p>
        '''
        
    except Exception as e:
        return f'''
        <h1>❌ Database Test Failed</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/">Back to Home</a></p>
        '''

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Simple admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple check - for testing only
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials! Try admin/admin123', 'error')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Login Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .login-form { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            button { background: #007bff; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
            button:hover { background: #0056b3; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 4px; }
            .flash.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .flash.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        </style>
    </head>
    <body>
        <div class="login-form">
            <h2>🔐 Admin Login Test</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username (try: admin)" required>
                <input type="password" name="password" placeholder="Password (try: admin123)" required>
                <button type="submit">Login</button>
            </form>
            <p><small>Test credentials: admin / admin123</small></p>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/dashboard')
def admin_dashboard():
    """Simple admin dashboard"""
    # For testing, skip authentication check
    
    try:
        conn = get_db_connection()
        
        # Get basic statistics
        users = conn.execute('SELECT COUNT(*) as count FROM user').fetchone()
        user_count = users['count'] if users else 0
        
        packages = conn.execute('SELECT COUNT(*) as count FROM package').fetchone()
        package_count = packages['count'] if packages else 0
        
        # Get recent users
        recent_users = conn.execute('''
            SELECT id, name, email, created_at, is_active
            FROM user 
            ORDER BY created_at DESC 
            LIMIT 5
        ''').fetchall()
        
        # Get packages
        all_packages = conn.execute('''
            SELECT id, name, price, daily_return_rate, duration_days, is_active
            FROM package 
            ORDER BY price ASC
        ''').fetchall()
        
        conn.close()
        
        # Build HTML response
        recent_users_html = ""
        for user in recent_users:
            status = "Active" if user['is_active'] else "Inactive"
            recent_users_html += f'''
            <tr>
                <td>{user['name']}</td>
                <td>{user['email']}</td>
                <td>{user['created_at']}</td>
                <td><span class="status-{status.lower()}">{status}</span></td>
            </tr>
            '''
        
        packages_html = ""
        for package in all_packages:
            status = "Active" if package['is_active'] else "Inactive"
            packages_html += f'''
            <tr>
                <td>{package['name']}</td>
                <td>₦{package['price']:,.2f}</td>
                <td>{package['daily_return_rate']}%</td>
                <td>{package['duration_days']} days</td>
                <td><span class="status-{status.lower()}">{status}</span></td>
            </tr>
            '''
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Dashboard Test</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }}
                .header {{ background: #343a40; color: white; padding: 1rem; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .stat-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #f8f9fa; font-weight: bold; }}
                .status-active {{ color: #28a745; font-weight: bold; }}
                .status-inactive {{ color: #dc3545; font-weight: bold; }}
                .nav {{ margin: 20px 0; }}
                .nav a {{ margin-right: 15px; color: #007bff; text-decoration: none; }}
                .nav a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎛️ Admin Dashboard - Working!</h1>
            </div>
            
            <div class="container">
                <div class="nav">
                    <a href="/">← Home</a>
                    <a href="/admin/login">Login</a>
                    <a href="/test-db">Test DB</a>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{user_count}</div>
                        <div>Total Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{package_count}</div>
                        <div>Total Packages</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">✅</div>
                        <div>Database Connected</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">🎉</div>
                        <div>Templates Working</div>
                    </div>
                </div>
                
                <div class="section">
                    <h3>📊 Recent Users</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Created</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recent_users_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="section">
                    <h3>📦 Packages</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Price</th>
                                <th>Daily Return</th>
                                <th>Duration</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {packages_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="section">
                    <h3>🔍 Diagnosis</h3>
                    <ul>
                        <li>✅ Flask is running properly</li>
                        <li>✅ Database connection working</li>
                        <li>✅ Templates can be rendered inline</li>
                        <li>✅ Data is being fetched from database</li>
                        <li>✅ Admin routes are accessible</li>
                    </ul>
                    <p><strong>If this works but the main admin panel doesn't, the issue might be:</strong></p>
                    <ul>
                        <li>Template file paths in admin_routes.py</li>
                        <li>Blueprint registration in main app.py</li>
                        <li>Import conflicts in the main app</li>
                        <li>Session/authentication issues</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        '''
        
    except Exception as e:
        return f'''
        <h1>❌ Dashboard Error</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/">Back to Home</a></p>
        '''

if __name__ == '__main__':
    print("🚀 Starting Simple Admin Test on port 5000...")
    print("📂 Database path:", DATABASE_PATH)
    print("📁 Template folder:", app.template_folder)
    app.run(debug=True, host='0.0.0.0', port=5000)
