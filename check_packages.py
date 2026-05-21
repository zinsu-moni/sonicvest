from app import app, db, Package

with app.app_context():
    packages = Package.query.all()
    print("=== Current Packages in Database ===")
    print(f"Total packages: {len(packages)}")
    print()
    
    for pkg in packages:
        # Calculate daily return amount
        daily_return_amount = pkg.price * (pkg.daily_return_rate / 100)
        # Calculate total return over duration
        total_return = daily_return_amount * pkg.duration_days
        
        print(f"Package: {pkg.name}")
        print(f"  Price: ₦{pkg.price:,.0f}")
        print(f"  Daily Rate: {pkg.daily_return_rate}%")
        print(f"  Daily Return: ₦{daily_return_amount:,.0f}")
        print(f"  Duration: {pkg.duration_days} days")
        print(f"  Total Return: ₦{total_return:,.0f}")
        print(f"  Active: {pkg.is_active}")
        print("-" * 50)
