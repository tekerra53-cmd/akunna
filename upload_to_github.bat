@echo off
REM GitHub Upload Script for Crop Disease Detector
REM Alternative to PowerShell script for CMD users

echo ========================================
echo Crop Disease Detector - GitHub Upload
echo ========================================
echo.

REM Configure Git
echo Configuring Git...
git config --global user.name "didi5-com"
git config --global user.email "lovedidi500@gmail.com"
echo.

REM Check status
echo Checking repository status...
git status
echo.

REM Add all files
echo Adding files to Git...
git add .
echo.

REM Commit changes
echo Creating commit...
git commit -m "Add comprehensive crop disease detection system with 60+ diseases"
echo.

REM Add remote
echo Adding GitHub remote...
git remote add origin https://github.com/didi5-com/crop-disease-detector.git 2>nul
if errorlevel 1 (
    echo Remote already exists, updating URL...
    git remote set-url origin https://github.com/didi5-com/crop-disease-detector.git
)
echo.

REM Push to GitHub
echo Pushing to GitHub...
echo You will be prompted for your GitHub credentials...
echo Username: didi5-com
echo Password: [Use your Personal Access Token]
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo Trying to create main branch...
    git branch -M main
    git push -u origin main
)

echo.
echo ========================================
echo Upload Complete!
echo ========================================
echo.
echo Your repository is now available at:
echo https://github.com/didi5-com/crop-disease-detector
echo.
pause
