"""
Admin database helper functions - works with PostgreSQL and SQLite
Uses SQLAlchemy for database operations
"""
from datetime import datetime
from sqlalchemy import text
from flask import current_app

# This will be initialized in app.py
db = None

def set_db(database):
    """Initialize the database connection"""
    global db
    db = database

def get_db():
    """Get the database instance with proper app context"""
    global db
    try:
        active_db = current_app.extensions.get('sqlalchemy')
        if active_db is not None:
            db = active_db
            return db
    except Exception:
        pass
    if db is None:
        # Try to import from app
        try:
            from app import db as app_db
            db = app_db
        except ImportError:
            pass
    return db

def execute_query(query, params=None):
    """Execute a raw SQL query and return results"""
    try:
        database = get_db()
        if database is None:
            print("❌ Database not initialized")
            return []
        if params:
            result = database.session.execute(text(query), params)
        else:
            result = database.session.execute(text(query))
        return result.fetchall()
    except Exception as e:
        print(f"❌ Query error: {e}")
        return []

def execute_scalar(query, params=None):
    """Execute a query and return a single scalar value"""
    try:
        database = get_db()
        if database is None:
            print("❌ Database not initialized")
            return None
        if params:
            result = database.session.execute(text(query), params)
        else:
            result = database.session.execute(text(query))
        return result.scalar()
    except Exception as e:
        print(f"❌ Query error: {e}")
        return None

def execute_one(query, params=None):
    """Execute a query and return one row"""
    try:
        database = get_db()
        if database is None:
            print("❌ Database not initialized")
            return None
        if params:
            result = database.session.execute(text(query), params)
        else:
            result = database.session.execute(text(query))
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        print(f"❌ Query error: {e}")
        return None

def execute_all(query, params=None):
    """Execute a query and return all rows as dicts"""
    try:
        database = get_db()
        if database is None:
            print("❌ Database not initialized")
            return []
        if params:
            result = database.session.execute(text(query), params)
        else:
            result = database.session.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        print(f"❌ Query error: {e}")
        return []

def execute_insert(query, params=None):
    """Execute an insert query"""
    try:
        database = get_db()
        if database is None:
            print("❌ Database not initialized")
            return False
        if params:
            database.session.execute(text(query), params)
        else:
            database.session.execute(text(query))
        database.session.commit()
        return True
    except Exception as e:
        print(f"❌ Insert error: {e}")
        database = get_db()
        if database:
            database.session.rollback()
        return False

def execute_update(query, params=None):
    """Execute an update query"""
    try:
        database = get_db()
        if database is None:
            print("❌ Database not initialized")
            return False
        if params:
            database.session.execute(text(query), params)
        else:
            database.session.execute(text(query))
        database.session.commit()
        return True
    except Exception as e:
        print(f"❌ Update error: {e}")
        database = get_db()
        if database:
            database.session.rollback()
        return False

def dict_from_row(row):
    """Convert database row to dictionary"""
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    try:
        return dict(row._mapping)
    except:
        return dict(row)
