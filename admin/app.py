from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
import sys

# Add parent directory to path to import from main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Configuration
app.secret_key = 'admin-secret-key-change-in-production'
app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'fintech.db')

# Template filters
@app.template_filter('format_number')
def format_number(value):
    """Format numbers with commas"""
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return "0"

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the admin dashboard.'

# Admin User Model
class AdminUser(UserMixin):
    def __init__(self, id, username, email, role, is_active, last_login):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self._is_active = is_active
        self.last_login = last_login
    
    @property
    def is_active(self):
        return self._is_active

@login_manager.user_loader
def load_user(user_id):
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email, role, is_active, last_login 
            FROM admin_users WHERE id = ? AND is_active = 1
        ''', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return AdminUser(*user_data)
        return None
    except:
        return None

# Database Helpers
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_admin_db():
    """Initialize admin tables"""
    try:
        print("🔧 Initializing admin database...")
        conn = get_db_connection()
        
        # Create admin_users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'admin',
                is_active BOOLEAN DEFAULT 1,
                last_login DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create default admin user if not exists
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM admin_users')
        if cursor.fetchone()[0] == 0:
            password_hash = generate_password_hash('admin123')
            conn.execute('''
                INSERT INTO admin_users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin@fintech.local', password_hash, 'super_admin'))
            print("✅ Default admin user created: admin / admin123")
        else:
            print("✅ Admin user already exists")
        
        conn.commit()
        conn.close()
        print("✅ Admin database initialization complete")
        
    except Exception as e:
        print(f"❌ Error initializing admin database: {e}")
        raise

def check_main_database():
    """Check if main database tables exist and provide helpful error message"""
    try:
        conn = get_db_connection()
        
        required_tables = ['users', 'transactions', 'packages', 'user_packages']
        missing_tables = []
        
        for table in required_tables:
            try:
                conn.execute(f'SELECT 1 FROM {table} LIMIT 1')
            except Exception:
                missing_tables.append(table)
        
        conn.close()
        
        if missing_tables:
            print(f"❌ Missing required tables: {', '.join(missing_tables)}")
            print("🔧 Please run the main application first to initialize the database:")
            print("   cd .. && python app.py")
            return False
        
        print("✅ Main database tables found")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

# Routes
@app.route('/')
@login_required
def dashboard():
    """Admin Dashboard"""
    conn = get_db_connection()
    
    # Get statistics with error handling
    stats = {
        'total_users': 0,
        'active_packages': 0,
        'pending_withdrawals': 0,
        'monthly_revenue': 0
    }
    
    recent_transactions = []
    gtr_payments = []
    
    try:
        # Total users
        result = conn.execute('SELECT COUNT(*) FROM users').fetchone()
        stats['total_users'] = result[0] if result else 0
        
        # Active packages
        result = conn.execute('''
            SELECT COUNT(*) FROM user_packages 
            WHERE status = 'active' AND end_date > datetime('now')
        ''').fetchone()
        stats['active_packages'] = result[0] if result else 0
        
        # Pending withdrawals
        result = conn.execute('''
            SELECT COUNT(*) FROM transactions 
            WHERE type = 'withdrawal' AND status = 'pending'
        ''').fetchone()
        stats['pending_withdrawals'] = result[0] if result else 0
        
        # Total revenue (last 30 days)
        result = conn.execute('''
            SELECT COALESCE(SUM(amount), 0) FROM transactions 
            WHERE transaction_type = 'deposit' 
            AND status = 'completed'
            AND datetime(timestamp) >= datetime('now', '-30 days')
        ''').fetchone()
        stats['monthly_revenue'] = result[0] if result else 0
        
        # Recent transactions
        recent_transactions = conn.execute('''
            SELECT t.*, u.username, u.email 
            FROM transactions t
            LEFT JOIN users u ON t.user_id = u.id
            ORDER BY t.timestamp DESC
            LIMIT 10
        ''').fetchall()
        
        # Recent GTR Bank payments
        gtr_payments = conn.execute('''
            SELECT t.*, u.username, u.email 
            FROM transactions t
            LEFT JOIN users u ON t.user_id = u.id
            WHERE t.description LIKE '%GTR Bank%'
            ORDER BY t.timestamp DESC
            LIMIT 5
        ''').fetchall()
        
    except Exception as e:
        print(f"Database error: {e}")
        flash(f'Database connection issue: {str(e)}. Please ensure the main application has been run first.', 'error')
    
    finally:
        conn.close()
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_transactions=recent_transactions,
                         gtr_payments=gtr_payments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin Login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user_data = conn.execute('''
            SELECT id, username, email, password_hash, role, is_active, last_login
            FROM admin_users WHERE username = ? AND is_active = 1
        ''', (username,)).fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = AdminUser(
                user_data['id'],
                user_data['username'],
                user_data['email'],
                user_data['role'],
                user_data['is_active'],
                user_data['last_login']
            )
            
            # Update last login
            conn = get_db_connection()
            conn.execute('''
                UPDATE admin_users SET last_login = datetime('now')
                WHERE id = ?
            ''', (user.id,))
            conn.commit()
            conn.close()
            
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Admin Logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def users():
    """User Management"""
    conn = get_db_connection()
    users_data = []
    
    try:
        # Get all users with their balances
        users_data = conn.execute('''
            SELECT u.*, 
                   0 as active_packages,
                   0 as total_deposits,
                   0 as total_withdrawals
            FROM users u
            ORDER BY u.created_at DESC
        ''').fetchall()
        
    except Exception as e:
        print(f"Database error in users route: {e}")
        flash(f'Database error: {str(e)}. Please ensure the main application database is properly initialized.', 'error')
    
    finally:
        conn.close()
    
    return render_template('users.html', users=users_data)

@app.route('/transactions')
@login_required
def transactions():
    """Transaction Management"""
    conn = get_db_connection()
    transactions_data = []
    
    try:
        # Get all transactions
        transactions_data = conn.execute('''
            SELECT t.*, u.username, u.email 
            FROM transactions t
            LEFT JOIN users u ON t.user_id = u.id
            ORDER BY t.timestamp DESC
            LIMIT 100
        ''').fetchall()
        
    except Exception as e:
        print(f"Database error in transactions route: {e}")
        flash(f'Database error: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return render_template('transactions.html', transactions=transactions_data)

@app.route('/gtr_payments')
@login_required
def gtr_payments():
    """GTR Bank Payments"""
    conn = get_db_connection()
    gtr_transactions = []
    
    try:
        # Get GTR Bank related transactions
        gtr_transactions = conn.execute('''
            SELECT t.*, u.username, u.email 
            FROM transactions t
            LEFT JOIN users u ON t.user_id = u.id
            WHERE t.description LIKE '%GTR Bank%'
            ORDER BY t.timestamp DESC
        ''').fetchall()
        
    except Exception as e:
        print(f"Database error in GTR payments route: {e}")
        flash(f'Database error: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return render_template('gtr_payments.html', transactions=gtr_transactions)

@app.route('/packages')
@login_required
def packages():
    """Package Management"""
    conn = get_db_connection()
    packages_data = []
    
    try:
        # Get all packages
        packages_data = conn.execute('''
            SELECT p.*, 0 as total_purchases
            FROM packages p
            ORDER BY p.name
        ''').fetchall()
        
    except Exception as e:
        print(f"Database error in packages route: {e}")
        flash(f'Database error: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return render_template('packages.html', packages=packages_data)

@app.route('/withdrawals')
@login_required
def withdrawals():
    """Withdrawal Management"""
    conn = get_db_connection()
    withdrawals_data = []
    
    try:
        # Get all withdrawal requests with user bank details
        withdrawals_data = conn.execute('''
            SELECT t.*, u.username, u.email, u.bank_name, u.account_number, u.account_name
            FROM transactions t
            LEFT JOIN users u ON t.user_id = u.id
            WHERE t.type = 'withdrawal'
            ORDER BY t.created_at DESC
        ''').fetchall()
            ORDER BY t.timestamp DESC
        ''').fetchall()
        
    except Exception as e:
        print(f"Database error in withdrawals route: {e}")
        flash(f'Database error: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return render_template('withdrawals.html', withdrawals=withdrawals_data)

@app.route('/approve_withdrawal/<int:transaction_id>', methods=['POST'])
@login_required
def approve_withdrawal(transaction_id):
    """Approve withdrawal request"""
    conn = get_db_connection()
    
    try:
        # Update transaction status
        conn.execute('''
            UPDATE transactions 
            SET status = 'completed'
            WHERE id = ? AND type = 'withdrawal'
        ''', (transaction_id,))
        
        conn.commit()
        flash('Withdrawal approved successfully!', 'success')
        
    except Exception as e:
        print(f"Error approving withdrawal: {e}")
        flash(f'Error approving withdrawal: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return redirect(url_for('withdrawals'))

@app.route('/reject_withdrawal/<int:transaction_id>', methods=['POST'])
@login_required
def reject_withdrawal(transaction_id):
    """Reject withdrawal request"""
    conn = get_db_connection()
    
    try:
        # Get transaction details to refund amount
        transaction = conn.execute('''
            SELECT user_id, amount FROM transactions 
            WHERE id = ? AND type = 'withdrawal'
        ''', (transaction_id,)).fetchone()
        
        if transaction:
            # Refund amount to withdrawal balance
            conn.execute('''
                UPDATE users 
                SET withdrawal_balance = withdrawal_balance + ?
                WHERE id = ?
            ''', (transaction['amount'], transaction['user_id']))
            
            # Update transaction status
            conn.execute('''
                UPDATE transactions 
                SET status = 'rejected'
                WHERE id = ?
            ''', (transaction_id,))
        
        conn.commit()
        flash('Withdrawal rejected and amount refunded!', 'warning')
        
    except Exception as e:
        print(f"Error rejecting withdrawal: {e}")
        flash(f'Error rejecting withdrawal: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return redirect(url_for('withdrawals'))

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for dashboard stats"""
    conn = get_db_connection()
    
    stats = {
        'total_users': 0,
        'active_packages': 0,
        'pending_withdrawals': 0,
        'today_revenue': 0
    }
    
    try:
        result = conn.execute('SELECT COUNT(*) FROM users').fetchone()
        stats['total_users'] = result[0] if result else 0
        
        result = conn.execute('''
            SELECT COUNT(*) FROM user_packages 
            WHERE status = 'active' AND end_date > datetime('now')
        ''').fetchone()
        stats['active_packages'] = result[0] if result else 0
        
        result = conn.execute('''
            SELECT COUNT(*) FROM transactions 
            WHERE transaction_type = 'withdrawal' AND status = 'pending'
        ''').fetchone()
        stats['pending_withdrawals'] = result[0] if result else 0
        
        result = conn.execute('''
            SELECT COALESCE(SUM(amount), 0) FROM transactions 
            WHERE transaction_type = 'deposit' 
            AND status = 'completed'
            AND date(timestamp) = date('now')
        ''').fetchone()
        stats['today_revenue'] = result[0] if result else 0
        
    except Exception as e:
        print(f"Error getting stats: {e}")
    
    finally:
        conn.close()
    
    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 Admin Dashboard Starting...")
    
    try:
        # Initialize admin database
        init_admin_db()
        print("✅ Admin database initialized")
        
        print("📊 Access at: http://localhost:5001")
        print("👤 Default Login: admin / admin123")
        print("🔧 Change default password after first login!")
        
        app.run(debug=True, port=5001, host='0.0.0.0')
        
    except Exception as e:
        print(f"❌ Error starting admin dashboard: {e}")
        import traceback
        traceback.print_exc()
