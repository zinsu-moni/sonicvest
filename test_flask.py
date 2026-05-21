"""
Minimal Flask app test for Python 3.13 compatibility
"""

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key'

@app.route('/')
def hello():
    return '<h1>✅ Flask is working!</h1><p>SQLAlchemy compatibility resolved!</p>'

@app.route('/test')
def test():
    try:
        from flask_sqlalchemy import SQLAlchemy
        return '<h1>✅ Flask-SQLAlchemy works!</h1><p>Ready to continue with fintech backend!</p>'
    except Exception as e:
        return f'<h1>❌ Error:</h1><p>{str(e)}</p>'

if __name__ == '__main__':
    print("🚀 Starting minimal Flask test...")
    print("💻 Visit: http://127.0.0.1:5000")
    print("🔬 Test SQLAlchemy: http://127.0.0.1:5000/test")
    app.run(debug=True, port=5000)
