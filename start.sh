#!/bin/bash

echo "========================================"
echo "   🎯 Lucky Draw Application"
echo "========================================"
echo ""
echo "Starting the application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Generate QR codes if they don't exist
if [ ! -f "static/images/upi_qr_static.png" ]; then
    echo "🎯 Generating UPI QR codes..."
    python generate_qr.py
    echo "✅ QR codes generated"
fi

# Start the application
echo "🚀 Starting Lucky Draw application..."
echo ""
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "📁 Data will be stored in: data/"
echo "💳 UPI ID: 9353539771@pthdfc"
echo "💰 Ticket Price: ₹5 per ticket"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python app.py
