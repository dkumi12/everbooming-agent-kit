# 🚀 Quick Deploy Commands - Copy & Paste

## Step 1: Clean Repository (Run in project root)
```bash
# Windows
.\cleanup.bat

# Mac/Linux  
chmod +x cleanup.sh && ./cleanup.sh
```

## Step 2: Review Changes
```bash
git status
# Verify venv/ and __pycache__/ are NOT listed
```

## Step 3: Commit Clean Repository
```bash
git add -A
git commit -m "chore: clean repository and add .gitignore for deployment"
```

## Step 4: Push to GitHub
```bash
# If first time, set remote:
git remote add origin https://github.com/YOUR_USERNAME/everbooming-agent-kit.git

# Push changes:
git push origin main
# (or: git push origin master)
```

## Step 5: Deploy to Railway
1. Go to: https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select "everbooming-agent-kit"
4. Add environment variables:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_DEFAULT_REGION=us-east-1
   ```
5. Wait 2-3 minutes for deployment
6. Get URL from Settings → Domains

## Step 6: Test Your Live Demo
```bash
# Open your Railway URL
# Try: "A mobile app for dog walkers"
# Verify all 7 agents execute
```

## Step 7: Update README
```bash
# Add your Railway URL to README.md
git add README.md
git commit -m "docs: add live demo link to README"
git push origin main
```

---

## 🎯 Expected Timeline
- Cleanup: 2 minutes
- Git operations: 2 minutes  
- Railway setup: 5 minutes
- Testing: 3 minutes
- **Total: ~12 minutes**

---

## ✅ Success Checklist
- [ ] cleanup.bat ran without errors
- [ ] Git shows .gitignore added
- [ ] Pushed to GitHub successfully
- [ ] Railway deployment succeeded
- [ ] Live URL accessible
- [ ] Test pipeline completed
- [ ] README updated with demo link

---

## 🆘 If Something Goes Wrong

**Build fails:**
```bash
# Check these files exist:
ls Dockerfile
ls requirements.txt
ls railway.json
```

**Can't push to GitHub:**
```bash
# Check remote:
git remote -v

# If empty, add it:
git remote add origin https://github.com/YOUR_USERNAME/everbooming-agent-kit.git
```

**Railway deployment fails:**
- Check Railway logs in dashboard
- Verify environment variables are set
- Ensure AWS credentials are correct

---

**📖 For detailed guide, see: RAILWAY_DEPLOY.md**
