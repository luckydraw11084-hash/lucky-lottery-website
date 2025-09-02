@echo off
echo.
echo ========================================
echo    🎯 Lucky Draw Setup Script
echo ========================================
echo.

echo 📦 Installing required packages...
pip install -r requirements.txt

echo.
echo 🔄 Generating QR code for mobile access...
python generate_website_qr.py

echo.
echo 🚀 Starting Lucky Draw Application...
echo.
echo ========================================
echo    🌐 Website URLs:
echo ========================================
echo.
echo 📱 Main Website:     http://localhost:5000
echo 🔧 Admin Dashboard:  http://localhost:5000/admin
echo.
echo ========================================
echo    🎯 Features Available:
echo ========================================
echo.
echo ✅ Real-time UPI payment verification
echo ✅ Admin dashboard with data management
echo ✅ One-click data reset for new lucky draws
echo ✅ Excel export for all bookings
echo ✅ Mobile QR code access
echo ✅ Beautiful warm beige design
echo ✅ Ticket selection animations
echo.
echo ========================================
echo    💡 How to Use:
echo ========================================
echo.
echo 1. 📱 Users scan QR code and access website
echo 2. 🎫 Select tickets and pay via UPI
echo 3. 🔧 Admin marks payment received in dashboard
echo 4. ✅ System automatically confirms booking
echo 5. 🎉 User gets success page instantly!
echo.
echo ========================================
echo    🔧 Admin Dashboard Features:
echo ========================================
echo.
echo 📊 View all bookings and statistics
echo 🔄 Reset all data for new lucky draw
echo 📥 Export bookings to Excel
echo 💰 Manage payments manually
echo 📱 Generate new QR codes
echo.
echo ========================================
echo.

python app.py
