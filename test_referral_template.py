#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template

# Create minimal Flask app for testing
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key'

@app.route('/test-referral')
def test_referral():
    """Test the referral template with mock data"""
    
    # Create mock user object
    class MockUser:
        def __init__(self):
            self.username = 'testuser'
            self.referral_code = 'TEST123'
            self.account_balance = 5000.0
            self.id = 1
    
    mock_user = MockUser()
    
    # Mock template data
    template_data = {
        'user': mock_user,
        'level1_earnings': 1000.0,
        'level2_earnings': 500.0,
        'level3_earnings': 200.0,
        'level1_commission': 240.0,  # 24% of 1000
        'level2_commission': 20.0,   # 4% of 500
        'level3_commission': 4.0,    # 2% of 200
        'level1_referrals': [],
        'level2_referrals': [],
        'level3_referrals': [],
        'total_referrals': 10,
        'active_referrals': 8,
        'total_commission': 264.0
    }
    
    print("🔍 Testing referral template rendering...")
    print(f"Template data: {template_data}")
    
    try:
        result = render_template('referral/index_new.html', **template_data)
        print(f"✅ Template rendered successfully! Length: {len(result)} characters")
        
        # Check if result is empty or just whitespace
        if not result.strip():
            return "❌ Template rendered but content is empty!"
        
        return result
        
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return f"Template Error: {str(e)}"

if __name__ == '__main__':
    print("🚀 Starting template test server on port 5001...")
    app.run(debug=True, host='127.0.0.1', port=5001)
