@echo off
echo ========================================
echo 🚀 GitHub Repository Setup
echo ========================================
echo.

echo 📋 This script will help you upload your code to GitHub
echo.

echo 🔧 Step 1: Check if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first:
    echo    Download from: https://git-scm.com/downloads
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
echo 📝 Step 3: Add all files to Git...
git add .
echo ✅ Files added to Git

echo.
echo 💾 Step 4: Create initial commit...
git commit -m "Initial commit - Lucky Draw Website with Real-time Payments"
echo ✅ Initial commit created

echo.
echo 🔗 Step 5: Add remote repository...
echo.
echo 📝 Please enter your GitHub username:
set /p username=Username: 
echo.
echo 📝 Please enter your repository name (default: lucky-draw-website):
set /p repo=Repository name: 
if "%repo%"=="" set repo=lucky-draw-website

git remote add origin https://github.com/%username%/%repo%.git
echo ✅ Remote repository added

echo.
echo 📤 Step 6: Push to GitHub...
git branch -M main
git push -u origin main
echo ✅ Code pushed to GitHub

echo.
echo ========================================
echo 🎉 GitHub Setup Complete!
echo ========================================
echo.
echo 📋 Your repository is now available at:
echo    https://github.com/%username%/%repo%
echo.
echo 🚀 Next Steps:
echo    1. Go to https://render.com
echo    2. Sign up with your GitHub account
echo    3. Create new Web Service
echo    4. Connect to your repository: %username%/%repo%
echo    5. Configure deployment settings
echo    6. Deploy!
echo.
echo 📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md
echo.
pause
