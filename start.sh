#!/bin/bash

echo "🚨 Starting DIMP - Disaster Intelligence Mapping Platform"
echo "========================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

echo ""
echo "📦 Setting up Backend..."
echo "------------------------"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Start backend in background
echo "Starting FastAPI backend on http://localhost:8000"
python main.py &
BACKEND_PID=$!

cd ..

echo ""
echo "🎨 Setting up Frontend..."
echo "------------------------"

cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies (this may take a few minutes)..."
    npm install
fi

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "🌐 Backend API: http://localhost:8000"
echo "🌐 Frontend UI: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Starting frontend..."
echo ""

# Start frontend
npm start

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
