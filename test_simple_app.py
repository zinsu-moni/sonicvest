#!/usr/bin/env python3
"""
Simple Flask app test
"""
from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = 'test-secret-key'

@app.route('/')
def home():
    return '<h1>Flask Test - Working!</h1><p><a href="/admin">Go to Admin</a></p>'

@app.route('/admin')
def admin_test():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Admin Panel Test</h1>
            <div class="card">
                <h3>✅ Flask is working!</h3>
                <p>This confirms that Flask can serve pages properly.</p>
            </div>
            <div class="card">
                <h3>🔍 Next Steps:</h3>
                <ul>
                    <li>Check if templates folder exists</li>
                    <li>Verify admin templates are in the right location</li>
                    <li>Test the main app.py</li>
                </ul>
            </div>
            <div class="card">
                <h3>📁 Template Structure Needed:</h3>
                <pre>templates/admin/login.html
templates/admin/dashboard.html
templates/admin/users.html
templates/admin/packages.html
templates/admin/transactions.html
templates/admin/withdrawals.html</pre>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Starting simple Flask test...")
    print("📂 Current directory:", os.getcwd())
    print("📁 Files in directory:", os.listdir('.'))
    app.run(debug=True, host='0.0.0.0', port=5001)
