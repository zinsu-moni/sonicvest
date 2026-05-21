"""
Database initialization script for Fintech platform
Creates tables and initial data
"""

from app import app, db, User, Package, Transaction, UserPackage, Withdrawal
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and sample data"""
    print("🗄️  Creating database tables...")
    
    with app.app_context():
        # Drop all existing tables and recreate
        db.drop_all()
        print("✅ Dropped existing tables")
        
        # Create all tables with correct structure
        db.create_all()
        print("✅ Database tables created with correct structure")
        
        # Create sample packages if they don't exist
        if Package.query.count() == 0:
            packages = [
                Package(
                    name='Starter Package',
                    description='Perfect for beginners - Start your investment journey',
                    price=5000.0,
                    daily_return_rate=2.86,
                    duration_days=30,
                    is_active=True
                ),
                Package(
                    name='Silver Package',
                    description='For growing investors - Build your wealth steadily',
                    price=25000.0,
                    daily_return_rate=2.86,
                    duration_days=30,
                    is_active=True
                ),
                Package(
                    name='Gold Package',
                    description='Premium investment option - Maximize your returns',
                    price=100000.0,
                    daily_return_rate=2.86,
                    duration_days=30,
                    is_active=True
                ),
                Package(
                    name='Platinum Package',
                    description='Ultimate investment package - For serious investors',
                    price=500000.0,
                    daily_return_rate=2.86,
                    duration_days=30,
                    is_active=True
                )
            ]
            
            for package in packages:
                db.session.add(package)
            
            db.session.commit()
            print("✅ Sample packages created")
        
        # Create admin user if doesn't exist
        admin_email = 'admin@fintech.com'
        if not User.query.filter_by(email=admin_email).first():
            admin_user = User(
                name='Admin User',
                email=admin_email,
                password_hash=generate_password_hash('admin123'),
                phone='+2347012345678',
                main_balance=1000000.0,  # Give admin some balance
                recharge_balance=500000.0
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Admin user created: {admin_email} / admin123")
        
        # Create test user
        test_email = 'test@example.com'
        if not User.query.filter_by(email=test_email).first():
            test_user = User(
                name='Test User',
                email=test_email,
                password_hash=generate_password_hash('test123'),
                phone='+2347098765432',
                main_balance=50000.0,
                recharge_balance=25000.0
            )
            db.session.add(test_user)
            db.session.commit()
            print(f"✅ Test user created: {test_email} / test123")
        
        print("\n🎉 Database initialization complete!")
        print("📊 Database summary:")
        print(f"   Users: {User.query.count()}")
        print(f"   Packages: {Package.query.count()}")
        print("\n🔑 Login credentials:")
        print("   Admin: admin@fintech.com / admin123")
        print("   Test User: test@example.com / test123")

if __name__ == '__main__':
    init_database()
