# GitHub Upload Script for Crop Disease Detector
# Run this script after installing Git

Write-Host "=== Crop Disease Detector - GitHub Upload Script ===" -ForegroundColor Green
Write-Host ""

# Configure Git (only needed once)
Write-Host "Configuring Git..." -ForegroundColor Yellow
git config --global user.name "didi5-com"
git config --global user.email "lovedidi500@gmail.com"

# Check current status
Write-Host ""
Write-Host "Checking repository status..." -ForegroundColor Yellow
git status

# Add all files
Write-Host ""
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Yellow
git commit -m "Add comprehensive crop disease detection system with 60+ diseases

- Expanded disease library from 17 to 60+ diseases
- Added support for wheat, soybean, cotton, apple, grape, banana, citrus
- Enhanced existing crops with more disease variants
- Each disease includes symptoms, treatment, and severity information
- Flask-based web application with ML inference
- SQLite database for disease knowledge and predictions
- Real-time crop disease detection and treatment recommendations"

# Check if remote exists
$remoteExists = git remote | Select-String -Pattern "origin"

if ($remoteExists) {
    Write-Host ""
    Write-Host "Remote 'origin' already exists. Updating..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/didi5-com/crop-disease-detector.git
} else {
    Write-Host ""
    Write-Host "Adding GitHub remote..." -ForegroundColor Yellow
    git remote add origin https://github.com/didi5-com/crop-disease-detector.git
}

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "You will be prompted for your GitHub credentials..." -ForegroundColor Cyan
Write-Host ""

# Try to push to main branch
git push -u origin main

# If main doesn't exist, try master
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Trying 'master' branch..." -ForegroundColor Yellow
    git branch -M main
    git push -u origin main
}

Write-Host ""
Write-Host "=== Upload Complete! ===" -ForegroundColor Green
Write-Host "Your repository should now be available at:" -ForegroundColor Cyan
Write-Host "https://github.com/didi5-com/crop-disease-detector" -ForegroundColor Cyan
