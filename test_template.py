#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/test')
def test_referral():
    """Test the referral template rendering"""
    print("🔍 Testing referral template...")
    
    # Mock data similar to what the real route provides
    mock_data = {
        'user': type('User', (), {
            'username': 'testuser',
            'referral_code': 'TEST123',
            'account_balance': 5000.0
        })(),
        'level1_earnings': 1000.0,
        'level2_earnings': 500.0,
        'level3_earnings': 200.0,
        'level1_commission': 240.0,
        'level2_commission': 20.0,
        'level3_commission': 4.0,
        'level1_referrals': 5,
        'level2_referrals': 3,
        'level3_referrals': 2,
        'total_referrals': 10,
        'active_referrals': 8,
        'total_commission': 264.0
    }
    
    print(f"🔍 Mock data: {mock_data}")
    
    try:
        rendered = render_template('referral/index_new.html', **mock_data)
        print(f"✅ Template rendered successfully! Length: {len(rendered)} characters")
        return rendered
    except Exception as e:
        print(f"❌ Template rendering error: {e}")
        return f"Template Error: {e}"

if __name__ == '__main__':
    print("🚀 Starting test server...")
    app.run(debug=True, host='127.0.0.1', port=5001)
