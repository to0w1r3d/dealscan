# How to Update DealScan

This guide shows you how to update your local DealScan installation with the latest changes from GitHub.

---

## Quick Update (Most Common)

```bash
# 1. Navigate to project directory
cd dealscan

# 2. Pull latest changes
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 4. Update dependencies (if requirements.txt changed)
pip install --upgrade -r requirements.txt

# 5. Test it works
python main.py --demo -q "laptop"
```

That's it! ✅

---

## Step-by-Step Instructions

### Step 1: Navigate to Project

```bash
cd ~/dealscan  # Or wherever you cloned it
```

### Step 2: Check Current Status

```bash
# See what branch you're on
git branch

# See if you have uncommitted changes
git status
```

**Expected output:**
```
On branch claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
nothing to commit, working tree clean
```

### Step 3: Pull Latest Changes

```bash
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
```

**Expected output:**
```
remote: Counting objects...
Unpacking objects: 100% (X/X), done.
From https://github.com/to0w1r3d/dealscan
   abc1234..def5678  claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq -> origin/claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
Updating abc1234..def5678
Fast-forward
 INSTALL.md           | 150 ++++++++++++++++++
 QUICKSTART.md        | 200 +++++++++++++++++++++++
 README.md            |  15 +-
 ...
```

### Step 4: Update Dependencies

**Activate virtual environment first:**

```bash
# Linux/Mac
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

**Update packages:**

```bash
pip install --upgrade -r requirements.txt
```

### Step 5: Verify Update

```bash
# Test with demo mode
python main.py --demo -q "laptop"

# Run tests
python production_test.py
```

If you see the DealScan banner and results, you're all set! ✅

---

## Common Scenarios

### Scenario 1: Clean Update (No Local Changes)

```bash
cd dealscan
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Scenario 2: You Made Local Changes

If you have uncommitted changes:

```bash
# Option A: Save your changes
git stash                    # Temporarily save changes
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
git stash pop                # Restore your changes

# Option B: Discard your changes
git reset --hard             # WARNING: Deletes all local changes
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
```

### Scenario 3: Merge Conflicts

If git says there are conflicts:

```bash
# View conflicted files
git status

# Edit conflicted files (look for <<<<<<, ======, >>>>>> markers)
# Then:
git add .
git commit -m "Resolved merge conflicts"
```

### Scenario 4: Fresh Install (Nuclear Option)

If things are really messed up:

```bash
# Backup any work you want to keep!

# Delete and re-clone
cd ..
rm -rf dealscan
git clone https://github.com/to0w1r3d/dealscan.git
cd dealscan
git checkout claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq

# Recreate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Checking for Updates

### See What's New

```bash
# Fetch latest info without updating
git fetch origin

# See what changed
git log HEAD..origin/claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq --oneline

# See detailed changes
git diff HEAD..origin/claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
```

### Check Current Version

```bash
# See your current commit
git log -1 --oneline

# See latest commit on GitHub
git ls-remote origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
```

---

## What Gets Updated

When you pull updates, you may get:

- ✅ **New features** - Additional scrapers, commands, etc.
- ✅ **Bug fixes** - Error handling improvements
- ✅ **Documentation** - New guides (like this one!)
- ✅ **Dependencies** - Updated requirements.txt
- ✅ **Configuration** - New settings or options

---

## After Updating

### Test Key Functionality

```bash
# Activate venv
source venv/bin/activate

# Test demo mode
python main.py --demo -q "laptop"

# Run test suite
python production_test.py

# Try different queries
python main.py --demo -q "gaming"
python main.py --demo -q "headphones"
```

### Check for New Documentation

Look for new `.md` files:

```bash
ls *.md
```

Recent additions:
- `INSTALL.md` - Virtual environment setup
- `QUICKSTART.md` - 5-minute quick start
- `DEALNEWS_ANALYSIS.md` - DealNews error analysis
- `UPDATE.md` - This file!

---

## Troubleshooting

### "fatal: not a git repository"

You're not in the right directory:

```bash
cd ~/dealscan  # Or wherever you cloned it
git status     # Should show git info
```

### "error: Your local changes... would be overwritten"

You have uncommitted changes:

```bash
# Save them
git stash

# Or discard them
git reset --hard
```

### "pip install fails"

Make sure venv is activated:

```bash
# Should show (venv) in prompt
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### "Module not found" errors after update

Reinstall dependencies:

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Git says "Already up to date" but you know there are changes

Fetch first:

```bash
git fetch origin
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
```

---

## Update Frequency

### When to Update

Update when:
- ✅ New features announced
- ✅ Bug fixes released
- ✅ Security updates available
- ✅ Documentation improvements
- ✅ You encounter issues (might be fixed)

### How Often

**Recommended:**
- Check weekly for updates
- Update before important use
- Update after seeing announcements

**Not recommended:**
- Updating in the middle of work
- Updating without testing
- Updating without reading changes

---

## Automatic Update Script

Create a quick update script:

**`update.sh` (Linux/Mac):**

```bash
#!/bin/bash
echo "Updating DealScan..."
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
source venv/bin/activate
pip install --upgrade -r requirements.txt
echo "Testing..."
python main.py --demo -q "test"
echo "Update complete!"
```

**Make it executable:**

```bash
chmod +x update.sh
./update.sh
```

**`update.bat` (Windows):**

```batch
@echo off
echo Updating DealScan...
git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq
call venv\Scripts\activate.bat
pip install --upgrade -r requirements.txt
echo Testing...
python main.py --demo -q "test"
echo Update complete!
pause
```

---

## Staying Informed

### GitHub Watch

Watch the repository for updates:
1. Go to https://github.com/to0w1r3d/dealscan
2. Click "Watch" → "All Activity"

### Check Commit History

```bash
# See recent changes
git log --oneline -10

# See what changed in a file
git log -p README.md
```

### Read Commit Messages

Each commit message explains what changed:

```bash
git log --oneline
# Look for messages like:
# "Add virtual environment installation guides"
# "Add DealNews error analysis"
```

---

## Rollback (If Needed)

If an update breaks something:

```bash
# See recent commits
git log --oneline -5

# Roll back to previous commit
git reset --hard abc1234  # Replace with commit hash

# Or go back 1 commit
git reset --hard HEAD~1
```

**Warning:** This deletes any local changes!

---

## Best Practices

1. ✅ **Always activate venv** before/after updating
2. ✅ **Read commit messages** to see what changed
3. ✅ **Test after updating** (use demo mode)
4. ✅ **Update dependencies** if requirements.txt changed
5. ✅ **Check for new docs** after updates

---

## Quick Reference

| Task | Command |
|------|---------|
| **Update code** | `git pull origin claude/product-deal-scraper-011CUMPZ2yJ5p3tzyur3YDcq` |
| **Update deps** | `pip install --upgrade -r requirements.txt` |
| **Check status** | `git status` |
| **See changes** | `git log --oneline -10` |
| **Test update** | `python main.py --demo -q "test"` |
| **Rollback** | `git reset --hard HEAD~1` |

---

## Need Help?

- **Git issues:** Check git documentation
- **Python issues:** Ensure venv is activated
- **Dependencies:** Try `pip install --upgrade pip` first
- **Other issues:** Check project documentation

---

**Last Updated:** 2025-10-22
**For:** DealScan v1.0+
