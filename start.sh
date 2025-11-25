#!/bin/bash

# USIU G6 SaaS Platform - Startup Script

echo "Starting USIU G6 SaaS Platform..."
echo ""

# Navigate to server directory
cd "$(dirname "$0")/server"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/lib/python3.*/site-packages/flask/__init__.py" ]; then
    echo " Installing dependencies..."
    pip install -r requirements.txt
    echo "Dependencies installed"
fi

# Start the Flask server
echo ""
echo "Starting Flask server..."
echo "Frontend: http://localhost:5000"
echo "Backend API: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
