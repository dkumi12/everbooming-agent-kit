#!/bin/bash
# Repository Cleanup Script for Everbooming Agent Kit
# Run this before deploying to Railway

echo "🧹 Starting repository cleanup..."

# Step 1: Delete temporary file 'v'
echo "📁 Removing temporary file 'v'..."
if [ -f "v" ]; then
    rm v
    echo "   ✅ Deleted 'v' file"
else
    echo "   ℹ️  File 'v' not found (already deleted)"
fi

# Step 2: Remove cached Python files
echo "🗑️  Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "   ✅ Python cache cleaned"

# Step 3: Check git status
echo "📊 Current git status:"
git status --short

# Step 4: Remove tracked items that should be ignored
echo ""
echo "🔄 Removing venv and cache from git tracking..."
git rm -r --cached venv 2>/dev/null || echo "   ℹ️  venv not tracked"
git rm -r --cached scripts/__pycache__ 2>/dev/null || echo "   ℹ️  __pycache__ not tracked"
git rm --cached v 2>/dev/null || echo "   ℹ️  v not tracked"

# Step 5: Add .gitignore
echo ""
echo "📝 Adding .gitignore..."
git add .gitignore
git add outputs/.gitkeep

# Step 6: Show what will be committed
echo ""
echo "📋 Files ready to commit:"
git status --short

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Review changes: git status"
echo "   2. Commit: git add -A && git commit -m 'chore: clean repository and add .gitignore'"
echo "   3. Push: git push origin main"
echo ""
echo "🚀 Then deploy to Railway!"
