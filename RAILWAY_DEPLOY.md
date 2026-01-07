# 🚂 Railway Deployment Guide - Everbooming Agent Kit

## Prerequisites Checklist
- [ ] AWS Bedrock credentials ready (Access Key ID + Secret Access Key)
- [ ] Mistral Large model enabled in AWS Bedrock (us-east-1)
- [ ] GitHub account with repository access
- [ ] Railway account (free tier works)
- [ ] Repository cleaned (run cleanup.bat)

---

## Step 1: Prepare Repository (5 minutes)

### 1.1 Run Cleanup Script
```bash
# On Windows
.\cleanup.bat

# On Mac/Linux
chmod +x cleanup.sh
./cleanup.sh
```

### 1.2 Verify Cleanup
```bash
# Check what will be committed
git status

# Should NOT see:
# - venv/
# - __pycache__/
# - v file
```

### 1.3 Commit Changes
```bash
git add -A
git commit -m "chore: clean repository and add .gitignore for Railway deployment"
```

### 1.4 Push to GitHub
```bash
# First time? Set remote
git remote add origin https://github.com/YOUR_USERNAME/everbooming-agent-kit.git

# Push
git push origin main
# Or if using 'master' branch:
git push origin master
```

---

## Step 2: Connect Railway (3 minutes)

### 2.1 Create Railway Account
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)
4. Authorize Railway to access your repositories

### 2.2 Deploy from GitHub

1. **Click "Deploy from GitHub repo"**
2. **Select your repository:** `everbooming-agent-kit`
3. **Railway auto-detects:**
   - ✅ Dockerfile found
   - ✅ railway.json configuration
   - ✅ Port 8501 for Streamlit

4. **Click "Deploy Now"**

---

## Step 3: Configure Environment Variables (2 minutes)

### 3.1 Add AWS Credentials

In Railway dashboard:
1. Click your deployed project
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

Add these variables:

```env
# Required
AWS_ACCESS_KEY_ID=AKIA..................
AWS_SECRET_ACCESS_KEY=wJalr..........................
AWS_DEFAULT_REGION=us-east-1

# Optional
CONTEXT7_API_KEY=ctx7_........................
ENABLE_CONTEXT7=true
DEBUG_MODE=false
DEFAULT_MODEL=mistral.mistral-large-2402-v1:0
```

### 3.2 Save and Redeploy
- Railway will automatically redeploy with new variables
- Wait ~2-3 minutes for build

---

## Step 4: Get Your Live Demo URL (1 minute)

### 4.1 Find Your URL
1. In Railway dashboard, click **"Settings"**
2. Under **"Domains"**, you'll see:
   ```
   https://everbooming-agent-kit-production.up.railway.app
   ```
3. Click to open and test!

### 4.2 Test the Deployment
1. Open your Railway URL
2. Enter a test idea: "A mobile app for dog walkers"
3. Click "Run Full Pipeline"
4. Verify all 7 agents execute successfully

---

## Step 5: Update README with Demo Link (1 minute)

### 5.1 Add Live Demo Badge

In your `README.md`, add at the top:

```markdown
# 🚀 Everbooming Agent Kit

[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://your-app.up.railway.app)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/everbooming-agent-kit)

> **Live Demo:** [https://your-app.up.railway.app](https://your-app.up.railway.app)
```

### 5.2 Commit and Push
```bash
git add README.md
git commit -m "docs: add live demo link"
git push origin main
```

---

## 🎯 Total Time: ~12 minutes
## 💰 Cost: $0 (Railway free tier: 500 hours/month)

---

## 🔧 Troubleshooting

### Build Fails

**Error:** `No Dockerfile found`
- **Solution:** Ensure Dockerfile is in root directory
- **Check:** `git ls-files | grep Dockerfile`

**Error:** `requirements.txt not found`
- **Solution:** Commit requirements.txt
- **Check:** `git ls-files | grep requirements.txt`

### Deployment Fails

**Error:** `Application failed to respond`
- **Solution:** Check logs in Railway dashboard
- **Common cause:** Missing environment variables

**Error:** `AWS credentials invalid`
- **Solution:** Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
- **Test locally:** `aws bedrock list-foundation-models`

### Application Errors

**Error:** `Mistral model not accessible`
- **Solution:** Enable Mistral Large in AWS Bedrock Console
- **Region:** Must be us-east-1

**Error:** `Context7 documentation unavailable`
- **Solution:** This is OK! It's optional
- **To enable:** Add CONTEXT7_API_KEY to Railway variables

---

## 📊 Monitoring Your Deployment

### Railway Dashboard
- **Logs:** Real-time application logs
- **Metrics:** CPU, Memory, Network usage
- **Deployments:** History of all deployments
- **Cost:** Free tier usage tracking

### Expected Behavior
- ✅ App loads in ~3 seconds
- ✅ First pipeline run takes ~2-3 minutes
- ✅ Each agent shows progress spinner
- ✅ All 7 outputs generate successfully
- ✅ Outputs saved to outputs/ folder

---

## ✅ Post-Deployment Checklist

- [ ] Railway URL is live and accessible
- [ ] Test pipeline runs successfully
- [ ] All 7 agents execute without errors
- [ ] Outputs generate in correct format
- [ ] No AWS credential errors in logs
- [ ] Updated README.md with demo link
- [ ] Committed and pushed all changes

---

## 🎉 Success Indicators

You're ready for job applications when:

1. **Demo URL works:** ✅ https://your-app.up.railway.app
2. **Full pipeline completes:** ✅ All 7 agents execute
3. **Professional outputs:** ✅ High-quality markdown docs
4. **GitHub updated:** ✅ Demo link in README
5. **No errors in logs:** ✅ Clean Railway logs

---

## 📱 Next Steps After Deployment

### 1. Create Demo Video (Optional but recommended)
- Record 2-minute walkthrough
- Upload to YouTube as unlisted
- Add to README and portfolio

### 2. LinkedIn Announcement
- Announce your live demo
- Tag relevant hashtags: #AWS #AI #MachineLearning
- Share Railway URL

### 3. Portfolio Update
- Add to projects section
- Include live demo link
- Highlight AWS + AI expertise

### 4. Apply to Jobs
- Include demo URL in applications
- Mention "deployed production AI system"
- Reference in technical interviews

---

## 🚨 Important Notes

### Free Tier Limits
- **Railway:** 500 hours/month (plenty for portfolio)
- **AWS Bedrock:** Pay per token (~$0.17/run)
- **Context7:** 5,000 requests/month free

### Cost Management
- Railway sleeps after 30min inactivity (free tier)
- First request after sleep takes ~30s to wake
- Monitor AWS costs in AWS Billing dashboard

### Security Best Practices
- ✅ Never commit .env file
- ✅ Rotate AWS keys every 90 days
- ✅ Use IAM user with minimal permissions
- ✅ Enable AWS CloudTrail for audit logs

---

## 📞 Support

### Railway Issues
- Railway Discord: https://discord.gg/railway
- Railway Docs: https://docs.railway.app

### AWS Bedrock Issues
- AWS Support: https://console.aws.amazon.com/support
- AWS Bedrock Docs: https://docs.aws.amazon.com/bedrock

### Project Issues
- GitHub Issues: https://github.com/YOUR_USERNAME/everbooming-agent-kit/issues

---

**🎊 Congratulations! Your AI Agent Kit is now live!**

**Demo URL:** `https://your-app.up.railway.app`
