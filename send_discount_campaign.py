import argparse
import os

from flask import render_template
from flask_mail import Message

from app import (
    app,
    mail,
    User,
    Package,
)


def _display_name(user):
    if getattr(user, "name", None):
        return user.name
    if getattr(user, "email", None) and "@" in user.email:
        return user.email.split("@", 1)[0]
    return "Investor"


def _build_package_offers(limit=4):
    packages = (
        Package.query.filter_by(is_active=True)
        .order_by(Package.price.asc())
        .limit(limit)
        .all()
    )
    return [
        {
            "name": pkg.name,
            "price": f"{pkg.price:,.0f}",
        }
        for pkg in packages
    ]


def _target_users(limit=None):
    query = (
        User.query.filter_by(is_admin=False, is_active=True)
        .filter(User.email.isnot(None))
        .filter(User.email != "")
        .filter(~User.user_packages_relation.any())
        .order_by(User.created_at.desc())
    )
    if limit:
        query = query.limit(limit)
    return query.all()


def _campaign_packages_url():
    base_url = (os.environ.get("APP_BASE_URL") or "").strip().rstrip("/")
    if base_url:
        return f"{base_url}/packages"

    server_name = (app.config.get("SERVER_NAME") or "").strip()
    if server_name:
        return f"https://{server_name}/packages"

    return "http://localhost:5000/packages"


def send_discount_campaign(limit=None, dry_run=False):
    if not app.config.get("MAIL_USERNAME") or not app.config.get("MAIL_PASSWORD"):
        print("ERROR: MAIL_USERNAME or MAIL_PASSWORD is not configured in .env")
        return 0, 0, 0

    package_offers = _build_package_offers()
    packages_url = _campaign_packages_url()

    users = _target_users(limit=limit)
    print(f"Found {len(users)} user(s) with no package purchases.")

    if dry_run:
        for user in users:
            print(f"DRY RUN -> {user.email}")
        return len(users), 0, 0

    sent = 0
    failed = 0
    for user in users:
        try:
            name = _display_name(user)
            html_body = render_template(
                "emails/discount_campaign.html",
                name=name,
                package_offers=package_offers,
                packages_url=packages_url,
            )
            text_body = render_template(
                "emails/discount_campaign.txt",
                name=name,
                package_offers=package_offers,
                packages_url=packages_url,
            )
            msg = Message(
                subject="Start Earning on Max Wealth Today",
                recipients=[user.email],
                sender=app.config.get("MAIL_DEFAULT_SENDER"),
                body=text_body,
                html=html_body,
            )
            mail.send(msg)
            sent += 1
            print(f"SENT -> {user.email}")
        except Exception as exc:
            failed += 1
            print(f"FAILED -> {user.email}: {exc}")

    return len(users), sent, failed


def main():
    parser = argparse.ArgumentParser(
        description="Send package reminder campaign email to users without package purchases."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of users to process.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List recipients without sending emails.",
    )
    args = parser.parse_args()

    with app.app_context():
        total, sent, failed = send_discount_campaign(limit=args.limit, dry_run=args.dry_run)
        print("--- Summary ---")
        print(f"Targets: {total}")
        print(f"Sent: {sent}")
        print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
