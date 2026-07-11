# How to Upload Your Crop Disease Detector to GitHub

## Prerequisites

Your GitHub details:
- **Username:** didi5-com
- **Email:** lovedidi500@gmail.com
- **Repository URL:** https://github.com/didi5-com/crop-disease-detector

## Step 1: Install Git

1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (just keep clicking "Next")
4. Restart your PowerShell/Terminal after installation

## Step 2: Create GitHub Repository

1. Go to: https://github.com/didi5-com
2. Click the green "New" button (or go to https://github.com/new)
3. Repository name: `crop-disease-detector`
4. Description: "AI-powered crop disease detection system with 60+ diseases"
5. Choose "Public" or "Private"
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 3: Get a Personal Access Token (Required for Authentication)

GitHub no longer accepts passwords for Git operations. You need a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Crop Disease Detector Upload"
4. Select scopes: Check "repo" (this gives full control of private repositories)
5. Click "Generate token" at the bottom
6. **IMPORTANT:** Copy the token immediately (you won't see it again!)
7. Save it somewhere safe (like a password manager)

## Step 4: Run the Upload Script

Open PowerShell in your project directory and run:

```powershell
cd "C:\Users\HP\Crop-Disease-Detector\Crop-Disease-Detector\Crop-Disease-Detector"
.\upload_to_github.ps1
```

When prompted for credentials:
- **Username:** didi5-com
- **Password:** [Paste your Personal Access Token here, NOT your GitHub password]

## Alternative: Manual Commands

If the script doesn't work, run these commands one by one:

```powershell
# Navigate to project
cd "C:\Users\HP\Crop-Disease-Detector\Crop-Disease-Detector\Crop-Disease-Detector"

# Configure Git
git config --global user.name "didi5-com"
git config --global user.email "lovedidi500@gmail.com"

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Add comprehensive crop disease detection system with 60+ diseases"

# Add remote
git remote add origin https://github.com/didi5-com/crop-disease-detector.git

# Push to GitHub
git push -u origin main
```

## Troubleshooting

### "git is not recognized"
- Git is not installed or not in PATH
- Restart your terminal after installing Git
- Try running: `where.exe git` to verify installation

### "remote origin already exists"
Run: `git remote set-url origin https://github.com/didi5-com/crop-disease-detector.git`

### "failed to push some refs"
The repository might already have content. Try:
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Authentication Failed
- Make sure you're using a Personal Access Token, not your password
- Generate a new token at: https://github.com/settings/tokens

## What Gets Uploaded

✅ Complete Flask application (`python_site/`)
✅ Expanded disease library (60+ diseases)
✅ README with setup instructions
✅ Requirements.txt with dependencies
✅ Database initialization scripts
✅ ML inference pipeline

❌ Virtual environment (.venv) - excluded
❌ Database files (*.db) - excluded
❌ Uploaded images - excluded
❌ Model checkpoints - excluded
❌ .env file - excluded

## After Upload

Your repository will be available at:
**https://github.com/didi5-com/crop-disease-detector**

You can then:
- Share the link with others
- Clone it on other machines
- Set up GitHub Pages for documentation
- Enable GitHub Actions for CI/CD
