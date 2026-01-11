# Files/Folders NOT Important to Repository

## 🗑️ Should Be Deleted/Ignored

### 1. **AWS CLI Directory (ENTIRE FOLDER)**
```
aws/
├── dist/           # AWS CLI binaries and dependencies
├── install         # AWS CLI installer script
├── README.md       # AWS CLI readme
└── THIRD_PARTY_LICENSES
```
**Reason:** This appears to be an AWS CLI installation bundle. Users should install AWS CLI independently via:
- Windows: `msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi`
- Mac/Linux: Package managers or official installers
- **Not needed** since the app uses boto3 Python library, not AWS CLI

**Action:** Delete entire `aws/` folder and add to `.gitignore`

---

### 2. **Virtual Environment**
```
venv/
├── Include/
├── Lib/
├── Scripts/
└── pyvenv.cfg
```
**Reason:** Virtual environments should never be committed to repos. Already in `.gitignore` but directory exists.

**Action:** Already ignored, but can be deleted locally and recreated with `python -m venv venv`

---

### 3. **Git Folder (Keep but don't track)**
```
.git/
```
**Reason:** Git metadata - already automatically ignored, just documenting here.

**Action:** No action needed - this is essential for version control

---

### 4. **Output Files (Sample outputs)**
```
outputs/
├── 01-BA.md
├── 02-PM.md
├── 02-PRD.md
├── 03-Arch.md
├── 04-PO.md
├── 05-SM.md
└── 06-TMA.md
```
**Reason:** These are sample/test outputs. `.gitignore` already excludes `outputs/*.md` except `.gitkeep`

**Action:** These will be auto-ignored on next commit. Keep `.gitkeep` only.

---

### 5. **Documentation Files (Redundant/Old)**
```
DEPLOYMENT_READY.md      # Old deployment notes
RAILWAY_DEPLOY.md        # Redundant with README.md
QUICK_DEPLOY.md          # Redundant with README.md
START_HERE.md            # Redundant if README is comprehensive
```
**Reason:** Multiple deployment guides create confusion. Should consolidate into main README.md

**Action:** 
- Review and merge important info into `README.md`
- Delete redundant files
- Keep only: `README.md`, `PROMPT_UPDATES.md`, `BEFORE_AFTER_COMPARISON.md`, `TESTING_GUIDE.md`

---

### 6. **Cleanup Scripts (Platform-specific redundancy)**
```
cleanup.bat              # Windows batch script
cleanup.sh               # Unix shell script
```
**Reason:** You mentioned "scripts folder has a bunch" - if these are redundant or unused, they can be removed.

**Action:** Check if these are used. If not, delete. Users can manually clean outputs folder.

---

### 7. **IDE/Editor Files (Should be in .gitignore)**
Already handled in `.gitignore`:
```
.vscode/
.idea/
*.swp
*.swo
```
**Action:** Already properly ignored ✅

---

## 📋 Recommended .gitignore Updates

Add these to `.gitignore`:

```bash
# AWS CLI (not needed for repo)
aws/

# Documentation (keep only essential)
DEPLOYMENT_READY.md
RAILWAY_DEPLOY.md
QUICK_DEPLOY.md
START_HERE.md

# Cleanup scripts (if not used)
cleanup.bat
cleanup.sh

# Railway-specific
railway.json  # (if you want to keep deployment config, remove this line)
```

---

## ✅ Essential Files to KEEP

### Core Application
```
app.py                          # Main Streamlit app
requirements.txt                # Python dependencies
Dockerfile                      # Container definition
railway.json                    # Railway deployment config (optional)
.dockerignore                   # Docker build exclusions
start.sh                        # Startup script
```

### Prompts & Scripts
```
prompts/
├── arch.md
├── ba.md
├── pm.md
├── po.md
├── prd.md
├── sm.md
└── tma.md

scripts/
├── __init__.py
├── arch_agent.py
├── ba_agent.py
├── context7_client.py
├── pm_agent.py
├── po_agent.py
├── prd_agent.py
├── sm_agent.py
├── task_master_agent.py
└── utils.py
```

### Configuration
```
.env.example                    # Environment variable template
.gitignore                      # Git exclusions
.streamlit/config.toml          # Streamlit settings
```

### Documentation (Essential only)
```
README.md                       # Main documentation
PROMPT_UPDATES.md              # Your recent updates
BEFORE_AFTER_COMPARISON.md    # Quality improvements doc
TESTING_GUIDE.md               # Testing instructions
```

### CI/CD
```
.github/workflows/              # GitHub Actions (if you have any)
```

---

## 🎯 Cleanup Commands

### Windows (PowerShell)
```powershell
# Remove AWS CLI folder
Remove-Item -Recurse -Force aws\

# Remove sample outputs (keep .gitkeep)
Remove-Item outputs\*.md

# Remove redundant docs (review first!)
Remove-Item DEPLOYMENT_READY.md, RAILWAY_DEPLOY.md, QUICK_DEPLOY.md, START_HERE.md

# Remove cleanup scripts if not used
Remove-Item cleanup.bat, cleanup.sh
```

### Mac/Linux
```bash
# Remove AWS CLI folder
rm -rf aws/

# Remove sample outputs
rm outputs/*.md

# Remove redundant docs (review first!)
rm DEPLOYMENT_READY.md RAILWAY_DEPLOY.md QUICK_DEPLOY.md START_HERE.md

# Remove cleanup scripts if not used
rm cleanup.bat cleanup.sh
```

---

## 📊 Summary

| Category | Files | Action |
|----------|-------|--------|
| **AWS CLI** | `aws/` entire folder | ❌ DELETE - Not needed |
| **Virtual Env** | `venv/` | ✅ Already ignored - can delete locally |
| **Sample Outputs** | `outputs/*.md` | ✅ Already ignored - auto-cleaned |
| **Redundant Docs** | 4 deployment guides | 🔍 REVIEW & DELETE after merging to README |
| **Cleanup Scripts** | `cleanup.bat`, `cleanup.sh` | 🔍 DELETE if unused |
| **IDE Files** | `.vscode/`, `.idea/` | ✅ Already ignored |

---

## 🚀 Final Repo Size After Cleanup

**Before:** ~150-200 MB (with AWS CLI binaries)
**After:** ~5-10 MB (clean Python project)

**Files count:**
- Before: ~100+ files
- After: ~30-40 essential files

This makes the repo:
- ✅ Faster to clone
- ✅ Easier to understand
- ✅ More professional
- ✅ Lower storage on GitHub
