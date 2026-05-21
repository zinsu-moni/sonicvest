from app import app, db, Package

with app.app_context():
    print("=== FF Packages Update Status ===")
    
    # Check current packages
    packages = Package.query.order_by(Package.price).all()
    print(f"Current packages in database: {len(packages)}")
    
    # Expected FF packages data
    expected_packages = [
        ('FF1', 3000, 785, 27475),
        ('FF2', 6000, 1550, 54250),
        ('FF3', 10000, 2650, 92750),
        ('FF4', 15000, 3800, 133000),
        ('FF5', 20000, 5650, 197750),
        ('FF6', 25000, 7500, 262500),
        ('FF7', 50000, 12550, 439250),
        ('FF8', 70000, 15250, 533750),
        ('FF9', 100000, 20500, 717500),
        ('FF10', 150000, 25500, 894250),
        ('FF11', 200000, 50500, 1767500),
        ('FF12', 250000, 55700, 1949500),
        ('FF13', 300000, 85000, 2975000),
    ]
    
    print("\nChecking if packages match expected values...")
    
    for name, expected_price, expected_daily, expected_total in expected_packages:
        pkg = Package.query.filter_by(name=name).first()
        if pkg:
            actual_daily = pkg.price * (pkg.daily_return_rate / 100)
            actual_total = actual_daily * pkg.duration_days
            
            price_match = abs(pkg.price - expected_price) < 1
            daily_match = abs(actual_daily - expected_daily) < 50  # Allow small variance
            
            status = "✅" if price_match and daily_match else "❌"
            print(f"{status} {name}: ₦{pkg.price:,.0f} → ₦{actual_daily:,.0f}/day → ₦{actual_total:,.0f} total")
        else:
            print(f"❌ {name}: Package not found in database")
    
    if len(packages) != len(expected_packages):
        print(f"\n⚠️  Database has {len(packages)} packages, expected {len(expected_packages)}")
        print("Consider running update_ff_packages.py to update the database")
    else:
        print(f"\n✅ All {len(expected_packages)} FF packages are in the database")
