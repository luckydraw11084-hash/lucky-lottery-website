#!/bin/bash

echo "🎯 Lucky Draw Setup and QR Code Generation"
echo "==========================================="

echo ""
echo "📦 Installing required packages..."
pip install -r requirements.txt

echo ""
echo "🔄 Generating QR Code for your website..."
python generate_website_qr.py

echo ""
echo "🚀 Starting the Lucky Draw application..."
python app.py
