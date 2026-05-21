#!/usr/bin/env python3
"""
Minimal Flask app to test admin dashboard
"""
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'test-key'

# Database path
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'fintech.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return '<h1>✅ Flask Working!</h1><p><a href="/admin/login">Admin Login</a> | <a href="/admin/dashboard">Admin Dashboard</a></p>'

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple test login
        if username == 'admin' and password == 'admin123':
            session['admin_id'] = 1
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid credentials')
    
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if logged in
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    # Get simple stats from database
    conn = get_db_connection()
    
    stats = {}
    try:
        # User count
        users = conn.execute('SELECT COUNT(*) as count FROM user').fetchone()
        stats['total_users'] = users['count'] if users else 0
        
        # Deposits
        deposits = conn.execute('SELECT SUM(amount) as total FROM "transaction" WHERE type = "deposit"').fetchone()
        stats['total_deposits'] = deposits['total'] if deposits and deposits['total'] else 0
        
        # Recent users
        recent_users_raw = conn.execute('''
            SELECT id, name as username, email, created_at
            FROM user 
            ORDER BY created_at DESC 
            LIMIT 5
        ''').fetchall()
        
        recent_users = []
        for user in recent_users_raw:
            recent_users.append({
                'username': user['username'],
                'email': user['email'],
                'registration_date': datetime.fromisoformat(user['created_at']) if user['created_at'] else None,
                'is_active': True
            })
        
    except Exception as e:
        print(f"Database error: {e}")
        stats = {'total_users': 0, 'total_deposits': 0}
        recent_users = []
    
    conn.close()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_users=recent_users,
                         recent_transactions=[],
                         pending_withdrawals=[],
                         active_packages=[],
                         admin={'username': 'admin'})

@app.route('/test-html')
def test_html():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test HTML</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 50px; }
            .container { max-width: 600px; margin: 0 auto; text-align: center; }
            .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Test HTML Page</h1>
            <div class="card">
                <h2>Static HTML Test</h2>
                <p>This page uses the same styling as the referral page to test if the issue is with the template.</p>
                <h3>Mock Referral Data:</h3>
                <p>📊 Total Referrals: <strong>5</strong></p>
                <p>💰 Total Commissions: <strong>₦264</strong></p>
                <p>👥 Active Members: <strong>3</strong></p>
                <p>🎯 Referral Code: <strong>TEST123</strong></p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Starting minimal test server...")
    print("📍 Test URLs:")
    print("   Home: http://127.0.0.1:5002/")
    print("   Test: http://127.0.0.1:5002/test")
    print("   HTML: http://127.0.0.1:5002/test-html")
    app.run(debug=True, host='127.0.0.1', port=5002)
