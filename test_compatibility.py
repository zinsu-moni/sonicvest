"""
Simple test to check SQLAlchemy compatibility with Python 3.13
"""

try:
    print("Testing basic imports...")
    
    import flask
    print(f"✅ Flask {flask.__version__} imported successfully")
    
    import sqlalchemy
    print(f"✅ SQLAlchemy {sqlalchemy.__version__} imported successfully")
    
    from flask_sqlalchemy import SQLAlchemy
    print("✅ Flask-SQLAlchemy imported successfully")
    
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy()
    db.init_app(app)
    
    print("✅ Flask-SQLAlchemy initialized successfully")
    print("✅ All compatibility tests passed!")
    print()
    print("🎉 Ready to run the fintech application!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("💡 Solution: Try installing newer versions:")
    print("   pip install --upgrade SQLAlchemy Flask-SQLAlchemy Flask")
