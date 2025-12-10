#!/bin/bash

# Discord Clone Backend Runner

echo "Starting Discord Clone Backend Server..."
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/requirements_installed.flag" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/requirements_installed.flag
    echo "Dependencies installed."
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "Please update .env with your configuration."
fi

# Start server
echo "Starting FastAPI server..."
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "=========================================="
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000