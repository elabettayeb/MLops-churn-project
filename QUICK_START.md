# 🚀 Quick Start: Push Your MLOps Project to GitHub

## 5-Minute Quick Start Guide

### Prerequisites
- GitHub account created (https://github.com)
- Git configured locally

---

## Step 1: Create GitHub Repository (2 minutes)

1. Go to **https://github.com/new**
2. **Repository name**: `MLops-churn-project`
3. Choose: **Public** or **Private**
4. **DO NOT** check "Initialize this repository with README"
5. Click **Create repository**
6. Copy the HTTPS URL (e.g., `https://github.com/YOUR_USERNAME/MLops-churn-project.git`)

---

## Step 2: Push Code to GitHub (2 minutes)

Open PowerShell/Terminal and run:

```bash
cd c:\Users\abettaieb\Desktop\MLops-churn-project

# Add the remote repository
git remote set-url origin https://github.com/YOUR_USERNAME/MLops-churn-project.git

# Verify remote is set
git remote -v

# Create/switch to main branch
git branch -M main

# Stage all changes (already done)
git add .

# Commit with message
git commit -m "Setup: Complete GitHub Actions CI/CD pipeline with DVC and MLflow"

# Push to GitHub
git push -u origin main
git push -u origin dev
```

---

## Step 3: Verify on GitHub (1 minute)

1. Go to **https://github.com/YOUR_USERNAME/MLops-churn-project**
2. Verify you see:
   - ✅ `.github/workflows/ml-pipeline.yml`
   - ✅ `src/` folder with Python scripts
   - ✅ `dvc.yaml`
   - ✅ `requirements.txt`
   - ✅ `GITHUB_SETUP_SUMMARY.md`
   - ✅ `docs/github-actions-setup.md`

---

## Step 4: Test the Workflow (Automatic)

Your workflow will automatically trigger on the next push.

To test immediately:

```bash
# Make a minor change
echo "" >> README.md

# Commit and push
git add README.md
git commit -m "Test: Trigger GitHub Actions workflow"
git push origin main
```

---

## Step 5: Monitor Workflow Execution

1. Go to your GitHub repo
2. Click **Actions** tab
3. Select **"MLOps Pipeline"** workflow
4. Watch it execute (takes 10-20 minutes)

---

## Optional: Configure Secrets (If Using Cloud Storage)

If you use S3 or another cloud storage for DVC:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add:
   ```
   Name: DVC_REMOTE_URL
   Value: s3://your-bucket/path
   
   Name: AWS_ACCESS_KEY_ID
   Value: your_access_key
   
   Name: AWS_SECRET_ACCESS_KEY
   Value: your_secret_key
   ```

---

## Check Your Work

After workflow completes:

✅ Navigate to **Actions** → Select the run → Scroll down to **Artifacts**

Download `mlflow-runs` to inspect metrics locally:

```bash
# Extract the artifact
# Then run:
mlflow ui --backend-store-uri mlruns
# Open: http://127.0.0.1:5000
```

---

## 📚 Documentation Files Created

| File | Purpose |
|------|---------|
| `SETUP_COMPLETE.md` | Complete checklist of everything done |
| `GITHUB_SETUP_SUMMARY.md` | Quick reference guide |
| `docs/github-actions-setup.md` | Detailed 6-part setup guide |

---

## Common Errors & Solutions

### Error: "fatal: remote origin already exists"
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/REPO.git
```

### Error: "fatal: 'origin' does not appear to be a 'git' repository"
```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO.git
```

### Workflow fails on dvc pull
- Remove the step if not using DVC remote storage
- Or configure `DVC_REMOTE_URL` secret

### Tests fail in CI
- Check Python version matches 3.10
- Review logs for specific test failures

---

## What Happens Automatically Now

Each time you **push to main**:

1. ✅ GitHub Actions triggers automatically
2. ✅ Python 3.10 + dependencies installed
3. ✅ DVC pipeline runs (data cleaning → feature engineering → training)
4. ✅ Model training with MLflow logging
5. ✅ Tests executed
6. ✅ Metrics exported
7. ✅ Artifacts uploaded
8. ✅ You get notified of success/failure

---

## Next: Development Workflow

For feature development:

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, test locally
# ...

# Commit and push
git push origin feature/my-feature

# Create Pull Request on GitHub
# Wait for CI/CD to pass
# Merge when ready
```

---

## Support

If you get stuck:
1. Check `docs/github-actions-setup.md` (comprehensive guide)
2. Review your workflow logs in **Actions** tab
3. Test locally: `dvc repro` + `python src/train.py`

---

**Ready to push? Use the commands from Step 2 above! 🚀**
