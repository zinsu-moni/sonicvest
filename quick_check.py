import sqlite3
conn = sqlite3.connect('fintech.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f'Found {len(tables)} tables:')
for t in tables:
    print(f'  - {t[0]}')
conn.close()
