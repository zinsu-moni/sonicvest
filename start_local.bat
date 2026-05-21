@echo off
echo ========================================
echo Starting Fintech Investment Platform
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo Starting Application Components
echo ========================================
echo.

REM Start the worker in a new window
echo Starting Income Distribution Worker...
start "Income Worker" cmd /k "venv\Scripts\activate.bat && python worker.py"

REM Wait a moment for worker to start
timeout /t 2 /nobreak > nul

REM Start the Flask application
echo Starting Flask Web Server...
echo.
echo ========================================
echo Application URLs:
echo ========================================
echo User Panel: http://localhost:5000
echo Admin Panel: http://localhost:5000/admin/login
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo Close all windows to stop all services
echo.

python app.py

pause
