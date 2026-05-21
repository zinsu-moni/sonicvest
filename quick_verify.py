from app import app, db, UserPackage

with app.app_context():
    # Get packages with income
    packages_with_income = UserPackage.query.filter(
        UserPackage.total_earned > 0
    ).all()
    
    print(f"Packages with income: {len(packages_with_income)}")
    for up in packages_with_income:
        print(f"  - {up.package.name} ({up.user.username}): N{up.total_earned:,.2f}")
