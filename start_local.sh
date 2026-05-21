#!/bin/bash

echo "========================================"
echo "Starting Fintech Investment Platform"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "Starting Application Components"
echo "========================================"
echo ""

# Start the worker in background
echo "Starting Income Distribution Worker..."
python worker.py > worker.log 2>&1 &
WORKER_PID=$!
echo "Worker PID: $WORKER_PID"

# Wait a moment for worker to start
sleep 2

# Start the Flask application
echo "Starting Flask Web Server..."
echo ""
echo "========================================"
echo "Application URLs:"
echo "========================================"
echo "User Panel: http://localhost:5000"
echo "Admin Panel: http://localhost:5000/admin/login"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo "Worker logs: worker.log"
echo ""

# Trap Ctrl+C to kill worker process
trap "echo 'Stopping worker...'; kill $WORKER_PID 2>/dev/null; exit" INT TERM

# Start Flask
python app.py

# Cleanup on exit
kill $WORKER_PID 2>/dev/null
