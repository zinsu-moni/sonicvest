from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is working!"

@app.route('/test-referral')
def test_referral():
    user = type('User', (), {
        'username': 'testuser',
        'referral_code': 'TEST123'
    })()
    
    data = {
        'user': user,
        'level1_earnings': 1000,
        'level2_earnings': 500,
        'level3_earnings': 200,
        'level1_commission': 240,
        'level2_commission': 20,
        'level3_commission': 4,
        'level1_referrals': [],
        'level2_referrals': [],
        'level3_referrals': [],
        'total_referrals': 5,
        'active_referrals': 3,
        'total_commission': 264
    }
    
    return render_template('referral/index_new.html', **data)

if __name__ == '__main__':
    print("🚀 Starting test Flask app on http://127.0.0.1:5001")
    app.run(debug=True, host='127.0.0.1', port=5001)
