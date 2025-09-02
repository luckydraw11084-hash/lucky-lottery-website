@echo off
echo ========================================
echo 🚀 Upload All Files to GitHub
echo ========================================
echo.

echo 📋 This script will upload ALL your files to your existing GitHub repository
echo.

echo 🔧 Step 1: Check if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo.
    echo 📥 Please install Git first:
    echo    1. Go to: https://git-scm.com/downloads
    echo    2. Download for Windows
    echo    3. Run the installer
    echo    4. Restart PowerShell
    echo    5. Run this script again
    echo.
    pause
    exit /b 1
)
echo ✅ Git is installed

echo.
echo 📁 Step 2: Initialize Git repository...
if not exist .git (
    git init
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

echo.
echo 📝 Step 3: Add ALL files to Git...
git add .
echo ✅ All files added to Git

echo.
echo 💾 Step 4: Create initial commit...
git commit -m "Complete Lucky Draw Website - All files uploaded"
echo ✅ Initial commit created

echo.
echo 🔗 Step 5: Add your existing GitHub repository...
echo.
echo 📋 Using your repository: https://github.com/luckydraw11084-hash/lucky-lottery-website.git
echo.

git remote add origin https://github.com/luckydraw11084-hash/lucky-lottery-website.git
echo ✅ Remote repository added

echo.
echo 📤 Step 6: Push ALL files to GitHub...
git branch -M main
git push -u origin main
echo ✅ All files pushed to GitHub

echo.
echo ========================================
echo 🎉 Upload Complete!
echo ========================================
echo.
echo 📋 Your repository is now available at:
echo    https://github.com/luckydraw11084-hash/lucky-lottery-website
echo.
echo 📁 Files uploaded:
echo    ✅ app_realtime.py (Main Flask app)
echo    ✅ templates/ (All HTML files)
echo    ✅ static/ (CSS, JS, images)
echo    ✅ data/ (Excel files)
echo    ✅ requirements.txt (Dependencies)
echo    ✅ Procfile (Deployment config)
echo    ✅ runtime.txt (Python version)
echo    ✅ README.md (Documentation)
echo    ✅ All guides and scripts
echo.
echo 🚀 Next Steps:
echo    1. Go to https://render.com
echo    2. Sign up with your GitHub account
echo    3. Create new Web Service
echo    4. Connect to: luckydraw11084-hash/lucky-lottery-website
echo    5. Deploy your website!
echo.
echo 📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md
echo.
pause
