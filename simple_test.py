from flask import Flask, render_template

app = Flask(__name__)

@app.route('/test')
def test():
    user = type('User', (), {
        'username': 'testuser',
        'referral_code': 'TEST123'
    })()
    
    data = {
        'user': user,
        'current_user': user,
        'level1_earnings': 0,
        'level2_earnings': 0,
        'level3_earnings': 0,
        'level1_commission': 0,
        'level2_commission': 0,
        'level3_commission': 0,
        'level1_referrals': [],
        'level2_referrals': [],
        'level3_referrals': [],
        'total_referrals': 0,
        'active_referrals': 0,
        'total_commission': 0
    }
    
    return render_template('referral/index_new.html', **data)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
