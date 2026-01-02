# GitHub Deployment Guide

## 🚀 Deploy to GitHub in 5 Steps

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Fill in repository details:
   - **Repository name**: `california-housing-predictor` (or your preferred name)
   - **Description**: "Machine learning app for predicting California housing prices using Random Forest and XGBoost"
   - Choose **Public** or **Private**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 2: Configure Git (First Time Only)

If you haven't configured Git before, run these commands:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace "Your Name" and "your.email@example.com" with your actual GitHub name and email.

### Step 3: Add Your Files to Git

```powershell
# Add all files
git add .

# Create first commit
git commit -m "Initial commit: California Housing Price Predictor"
```

### Step 4: Link to GitHub Repository

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your GitHub username and repository name:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
```

### Step 5: Push to GitHub

```powershell
git push -u origin main
```

You'll be prompted to enter your GitHub credentials. If you have 2FA enabled, you'll need to use a **Personal Access Token** instead of your password.

---

## 🔐 Creating GitHub Personal Access Token

If you need a personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Housing Predictor Deployment")
4. Select scopes: Check **repo** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing to GitHub

---

## 📝 Future Updates

After the initial deployment, to update your GitHub repository:

```powershell
# Add changed files
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

---

## 🌐 Deploy to Cloud Platforms

### Option 1: Heroku

```bash
# Install Heroku CLI
# Create a Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: Render

1. Go to [Render](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure:
   - Build Command: `pip install -r requirements_new.txt`
   - Start Command: `gunicorn app:app`

### Option 3: Railway

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect and deploy

### Option 4: Docker Deployment

```bash
# Build Docker image
docker build -t housing-predictor .

# Run container
docker run -p 5000:5000 housing-predictor

# Or deploy to Docker Hub
docker tag housing-predictor YOUR_USERNAME/housing-predictor
docker push YOUR_USERNAME/housing-predictor
```

---

## 📊 GitHub Repository Best Practices

### Add a LICENSE

Consider adding a license file (MIT is common for open source):

```powershell
# Download MIT License
curl https://opensource.org/licenses/MIT -o LICENSE
```

### Add Badges to README

Add status badges to your README.md:

```markdown
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### Enable GitHub Pages (Optional)

If you want to host documentation:

1. Go to repository Settings → Pages
2. Select branch: `main`
3. Select folder: `/docs` or root
4. Save

---

## ✅ Verify Your Deployment

After pushing to GitHub, verify:

1. ✅ All files are visible on GitHub
2. ✅ README.md displays correctly
3. ✅ .gitignore is working (venv/ should not be uploaded)
4. ✅ Repository has a description
5. ✅ Topics/tags are added (python, flask, machine-learning, xgboost)

---

## 🔧 Troubleshooting

**Error: "failed to push some refs"**
```powershell
git pull origin main --rebase
git push -u origin main
```

**Error: "Permission denied"**
- Make sure you're using the correct GitHub username
- Use a Personal Access Token instead of password
- Check if you have write access to the repository

**Large files rejected**
- Models might be too large for GitHub (100MB limit)
- Use Git Large File Storage (LFS):
```powershell
git lfs install
git lfs track "*.joblib"
git add .gitattributes
git commit -m "Configure Git LFS"
```

---

## 📧 Need Help?

- GitHub Documentation: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- Issues: Open an issue on your repository

---

## 🎉 You're Done!

Your California Housing Price Predictor is now on GitHub and ready to share with the world!