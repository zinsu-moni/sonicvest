#!/usr/bin/env python3
"""
Migration: Align user_package table schema with the ORM model used in app.py.

This script will:
- Detect legacy columns (purchase_date, expiry_date, total_earnings, last_income_date)
- Add missing columns (amount_invested, daily_return, start_date, end_date, total_earned, last_payout, is_active)
- Backfill new columns from legacy columns and related package price/rate when possible

It targets the SQLite DB at fintech/fintech.db (same file used by admin_routes and app.py).
"""

import os
import sqlite3
from datetime import datetime


def get_db_paths() -> list[str]:
    """Return list of DB paths to migrate (package DB and instance DB if present)."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    paths = [os.path.join(base_dir, 'fintech.db')]
    instance_db = os.path.join(base_dir, 'instance', 'fintech.db')
    if os.path.exists(instance_db):
        paths.append(instance_db)
    return paths


def column_exists(cursor: sqlite3.Cursor, table: str, column: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def table_exists(cursor: sqlite3.Cursor, table: str) -> bool:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None


def migrate_user_package(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    if not table_exists(cur, 'user_package'):
        print("❌ Table 'user_package' does not exist. Nothing to migrate.")
        return

    # Gather existing columns
    cur.execute("PRAGMA table_info(user_package)")
    existing_cols = [r[1] for r in cur.fetchall()]
    print("Current user_package columns:", existing_cols)

    # Plan column additions
    add_plan = []
    if 'amount_invested' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN amount_invested FLOAT DEFAULT 0.0")
    if 'daily_return' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN daily_return FLOAT DEFAULT 0.0")
    if 'start_date' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN start_date DATETIME")
    if 'end_date' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN end_date DATETIME")
    if 'total_earned' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN total_earned FLOAT DEFAULT 0.0")
    if 'last_payout' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN last_payout DATETIME")
    if 'is_active' not in existing_cols:
        add_plan.append("ALTER TABLE user_package ADD COLUMN is_active BOOLEAN DEFAULT 1")

    if add_plan:
        print("Adding missing columns to user_package…")
        for stmt in add_plan:
            print("  ", stmt)
            cur.execute(stmt)
        conn.commit()
        print("✅ Columns added where needed.")
    else:
        print("✅ All required columns already exist.")

    # Backfill from legacy columns when present
    # Map legacy -> new
    legacy_cols = {
        'purchase_date': 'start_date',
        'expiry_date': 'end_date',
        'total_earnings': 'total_earned',
        'last_income_date': 'last_payout',
    }

    for legacy, newcol in legacy_cols.items():
        if column_exists(cur, 'user_package', legacy) and column_exists(cur, 'user_package', newcol):
            # Only update rows where newcol is NULL
            update_sql = f"UPDATE user_package SET {newcol} = {legacy} WHERE {newcol} IS NULL"
            print(f"Backfilling {newcol} from {legacy}…")
            cur.execute(update_sql)
    conn.commit()

    # Backfill amount_invested from related package.price if possible
    if column_exists(cur, 'user_package', 'amount_invested'):
        print("Backfilling amount_invested from package.price where 0 or NULL…")
        cur.execute(
            """
            UPDATE user_package
            SET amount_invested = (
                SELECT p.price FROM package p WHERE p.id = user_package.package_id
            )
            WHERE (amount_invested IS NULL OR amount_invested = 0)
        """
        )
        conn.commit()

    # Backfill daily_return using amount_invested * (package.daily_return_rate/100)
    if column_exists(cur, 'user_package', 'daily_return'):
        print("Backfilling daily_return from amount_invested and package.daily_return_rate…")
        cur.execute(
            """
            UPDATE user_package
            SET daily_return = (
                COALESCE(
                    (
                        SELECT ROUND( up.amount_invested * (p.daily_return_rate / 100.0), 6 )
                        FROM package p
                        JOIN user_package up ON up.id = user_package.id AND p.id = up.package_id
                    ),
                    daily_return
                )
            )
            WHERE daily_return IS NULL OR daily_return = 0
        """
        )
        conn.commit()

    # Ensure end_date present if start_date + duration available
    # We can compute end_date = start_date + duration_days from package if start_date exists and end_date is NULL
    if column_exists(cur, 'user_package', 'start_date') and column_exists(cur, 'user_package', 'end_date'):
        print("Backfilling end_date using start_date + package.duration_days where missing…")
        # SQLite doesn't support INTERVAL; use julianday math
        cur.execute(
            """
            UPDATE user_package
            SET end_date = (
                SELECT datetime(up.start_date, '+' || p.duration_days || ' days')
                FROM package p
                JOIN user_package up ON up.id = user_package.id AND p.id = up.package_id
            )
            WHERE end_date IS NULL AND start_date IS NOT NULL
        """
        )
        conn.commit()

    print("\nVerifying final user_package columns…")
    cur.execute("PRAGMA table_info(user_package)")
    cols = [r[1] for r in cur.fetchall()]
    print("✅ New user_package columns:", cols)


def migrate_transaction(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    if not table_exists(cur, 'transaction'):
        print("❌ Table 'transaction' does not exist. Nothing to migrate.")
        return

    cur.execute("PRAGMA table_info(\"transaction\")")
    cols = [r[1] for r in cur.fetchall()]
    print("Current transaction columns:", cols)

    add_tx_plan = []
    if 'status' not in cols:
        add_tx_plan.append("ALTER TABLE \"transaction\" ADD COLUMN status VARCHAR(20) DEFAULT 'pending'")
    if 'reference' not in cols:
        add_tx_plan.append("ALTER TABLE \"transaction\" ADD COLUMN reference VARCHAR(100)")

    if add_tx_plan:
        print("Adding missing columns to transaction…")
        for stmt in add_tx_plan:
            print("  ", stmt)
            cur.execute(stmt)
        conn.commit()
        print("✅ Transaction columns added where needed.")
    else:
        print("✅ Transaction table already has required columns.")


def migrate_withdrawal(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    if not table_exists(cur, 'withdrawal'):
        print("❌ Table 'withdrawal' does not exist. Nothing to migrate.")
        return

    cur.execute("PRAGMA table_info(withdrawal)")
    cols = [r[1] for r in cur.fetchall()]
    print("Current withdrawal columns:", cols)

    add_w_plan = []
    if 'reason' not in cols:
        add_w_plan.append("ALTER TABLE withdrawal ADD COLUMN reason VARCHAR(200)")
    if 'processed_by' not in cols:
        add_w_plan.append("ALTER TABLE withdrawal ADD COLUMN processed_by INTEGER")

    if add_w_plan:
        print("Adding missing columns to withdrawal…")
        for stmt in add_w_plan:
            print("  ", stmt)
            cur.execute(stmt)
        conn.commit()
        print("✅ Withdrawal columns added where needed.")
    else:
        print("✅ Withdrawal table already has required columns.")


def main():
    any_migrated = False
    result_code = 0
    for db_path in get_db_paths():
        print(f"🔧 Migrating database: {db_path}")
        if not os.path.exists(db_path):
            print("  ⚠️  Skipping (not found)")
            continue
        try:
            conn = sqlite3.connect(db_path)
            migrate_user_package(conn)
            migrate_transaction(conn)
            migrate_withdrawal(conn)
            conn.commit()
            conn.close()
            any_migrated = True
            print("  ✅ Done for:", db_path)
        except Exception as e:
            print(f"  ❌ Migration failed for {db_path}: {e}")
            result_code = 2

    if any_migrated and result_code == 0:
        print("\n🎉 Migration completed successfully for all detected databases!")
    elif not any_migrated:
        print("\n❌ No databases migrated (none found).")
        result_code = 1
    return result_code


if __name__ == '__main__':
    raise SystemExit(main())
