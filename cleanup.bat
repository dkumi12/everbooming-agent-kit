@echo off
REM Repository Cleanup Script for Everbooming Agent Kit (Windows)
REM Run this before deploying to Railway

echo 🧹 Starting repository cleanup...
echo.

REM Step 1: Delete temporary file 'v'
echo 📁 Removing temporary file 'v'...
if exist v (
    del /q v
    echo    ✅ Deleted 'v' file
) else (
    echo    ℹ️  File 'v' not found (already deleted)
)

REM Step 2: Remove cached Python files
echo 🗑️  Removing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo    ✅ Python cache cleaned

REM Step 3: Check git status
echo 📊 Current git status:
git status --short

REM Step 4: Remove tracked items that should be ignored
echo.
echo 🔄 Removing venv and cache from git tracking...
git rm -r --cached venv 2>nul
if errorlevel 1 echo    ℹ️  venv not tracked
git rm -r --cached scripts\__pycache__ 2>nul
if errorlevel 1 echo    ℹ️  __pycache__ not tracked
git rm --cached v 2>nul
if errorlevel 1 echo    ℹ️  v not tracked

REM Step 5: Add .gitignore
echo.
echo 📝 Adding .gitignore...
git add .gitignore
git add outputs\.gitkeep

REM Step 6: Show what will be committed
echo.
echo 📋 Files ready to commit:
git status --short

echo.
echo ✅ Cleanup complete!
echo.
echo 📝 Next steps:
echo    1. Review changes: git status
echo    2. Commit: git add -A ^&^& git commit -m "chore: clean repository and add .gitignore"
echo    3. Push: git push origin main
echo.
echo 🚀 Then deploy to Railway!
echo.
pause
