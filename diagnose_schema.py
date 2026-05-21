import os, sqlite3
BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'fintech.db')
print('DB:', DB, 'exists=', os.path.exists(DB))
conn = sqlite3.connect(DB)
cur = conn.cursor()
for tbl in ('package','user_package','transaction','withdrawal','user'):
    try:
        cur.execute(f'PRAGMA table_info({tbl})')
        rows = cur.fetchall()
        cols = [r[1] for r in rows]
        print(f'{tbl}:', cols)
        for cid, name, ctype, notnull, dflt_value, pk in rows:
            if notnull or dflt_value is not None:
                print(f'  - {name}: type={ctype}, notnull={notnull}, default={dflt_value}, pk={pk}')
    except Exception as e:
        print(f'{tbl}: ERROR', e)
conn.close()
