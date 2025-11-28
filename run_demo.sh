#!/bin/bash
# Quick start script for demo mode

echo "=========================================="
echo "  Cyber Defense Dashboard - Demo Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi
echo "✅ Python 3 found"

# Check/Install dependencies
echo ""
echo "Checking dependencies..."

if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask installed"
else
    echo "📦 Installing Flask..."
    pip install flask
fi

if python3 -c "import psutil" 2>/dev/null; then
    echo "✅ psutil installed"
else
    echo "📦 Installing psutil..."
    pip install psutil
fi

echo ""
echo "=========================================="
echo "  Starting Demo Mode..."
echo "=========================================="
echo ""
echo "🎭 Demo mode uses simulated data"
echo "📊 Dashboard will be at: http://localhost:7000"
echo "🛑 Press Ctrl+C to stop"
echo ""

# Start demo
python3 demo_mode.py
