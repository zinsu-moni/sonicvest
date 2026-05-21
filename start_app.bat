@echo off
cd /d "c:\Users\zinsu\Downloads\fintech"
echo Adding is_admin column to database...
echo.

python -c "import sqlite3; c=sqlite3.connect('instance/fintech.db'); c.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0'); c.commit(); print('✓ Added is_admin column successfully'); c.close()" 2>nul || echo Column already exists

echo.
echo Trying to start Flask app...
python app.py
