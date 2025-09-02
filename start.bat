@echo off
echo ========================================
echo    🎯 Lucky Draw Application
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Generate QR codes if they don't exist
if not exist "static\images\upi_qr_static.png" (
    echo 🎯 Generating UPI QR codes...
    python generate_qr.py
    echo ✅ QR codes generated
)

REM Start the application
echo 🚀 Starting Lucky Draw application...
echo.
echo 🌐 Open your browser and go to: http://localhost:5000
echo 📁 Data will be stored in: data/
echo 💳 UPI ID: 9353539771@pthdfc
echo 💰 Ticket Price: ₹5 per ticket
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py

pause
