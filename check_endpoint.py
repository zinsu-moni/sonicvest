from fintech.app import app
from flask import url_for

if __name__ == '__main__':
    with app.test_request_context():
        print('index ->', url_for('index'))
