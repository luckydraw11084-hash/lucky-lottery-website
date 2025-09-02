# 🚀 Manual Git Commands to Upload All Files

## Step 1: Install Git

1. Go to: https://git-scm.com/downloads
2. Download for Windows
3. Install and restart PowerShell

## Step 2: Navigate to Project Directory

```powershell
cd "S:\DRAW L\lucky_draw"
```

## Step 3: Run These Commands One by One

```powershell
# Initialize Git repository
git init

# Add ALL files to Git
git add .

# Create commit with all files
git commit -m "Complete Lucky Draw Website - All files uploaded"

# Add your existing GitHub repository
git remote add origin https://github.com/luckydraw11084-hash/lucky-lottery-website.git

# Push all files to GitHub
git branch -M main
git push -u origin main
```

## Files That Will Be Uploaded:

✅ app_realtime.py (Main Flask application)
✅ templates/ (All HTML templates)
✅ static/ (CSS, JS, images)
✅ data/ (Excel files and data)
✅ requirements.txt (Python dependencies)
✅ Procfile (Deployment configuration)
✅ runtime.txt (Python version)
✅ README.md (Documentation)
✅ DEPLOYMENT_GUIDE.md (Deployment instructions)
✅ All setup scripts (.bat files)
✅ All documentation files (.md files)

## Alternative: Use the Automated Script

Double-click `upload_to_github.bat` in your lucky_draw folder and follow the prompts.

## After Upload:

1. Go to your GitHub repository URL: https://github.com/luckydraw11084-hash/lucky-lottery-website
2. Verify all files are uploaded
3. Follow DEPLOYMENT_GUIDE.md to deploy to Render
