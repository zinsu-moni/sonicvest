"""
Vercel serverless function entry point
This wraps the Flask app for Vercel's serverless environment
"""

from app import app

# Vercel expects the Flask app to be called 'app'
# This file is needed because Vercel runs functions in isolation
if __name__ != "__main__":
    # Initialize database on module import (for Vercel cold starts)
    try:
        with app.app_context():
            from app import db
            db.create_all()
            print("✅ Database initialized for Vercel")
    except Exception as e:
        print(f"⚠️ Database initialization: {e}")
