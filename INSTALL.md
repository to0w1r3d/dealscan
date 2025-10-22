# Installation Guide

## Quick Start (Recommended)

This guide walks you through setting up DealScan using a **virtual environment** (best practice for Python projects).

---

## Step 1: Prerequisites

Ensure you have:
- **Python 3.7+** installed
- **git** installed (for cloning)
- **pip** (comes with Python)

Check your Python version:
```bash
python3 --version
# Should show: Python 3.7.x or higher
```

---

## Step 2: Clone the Repository

```bash
git clone https://github.com/to0w1r3d/dealscan.git
cd dealscan
```

---

## Step 3: Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Makes the project portable and reproducible
- Easy to clean up (just delete the venv folder)

### Linux / macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv)
```

### Windows (Command Prompt)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat

# Your prompt should now show (venv)
```

### Windows (PowerShell)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1

# Note: You may need to run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Verification:** Your command prompt should now show `(venv)` at the beginning.

---

## Step 4: Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

You should see:
```
Collecting requests>=2.31.0
Collecting beautifulsoup4>=4.12.0
Collecting lxml>=4.9.0
Collecting colorama>=0.4.6
Collecting python-dateutil>=2.8.2
...
Successfully installed beautifulsoup4-x.x.x colorama-x.x.x lxml-x.x.x ...
```

---

## Step 5: Verify Installation

```bash
# Check if main.py runs
python main.py --help

# Run demo mode
python main.py --demo -q "laptop"
```

If you see the DealScan banner and search results, you're all set! ✅

---

## Step 6: Daily Usage

### Activating the Environment

**Every time** you open a new terminal to use DealScan, activate the virtual environment first:

**Linux/Mac:**
```bash
cd dealscan
source venv/bin/activate
```

**Windows:**
```bash
cd dealscan
venv\Scripts\activate
```

### Running DealScan

```bash
# Demo mode (works immediately)
python main.py --demo -q "your search"

# Live mode (requires residential IP)
python main.py -q "your search"
```

### Deactivating the Environment

When you're done:
```bash
deactivate
```

---

## Alternative: System-Wide Installation (Not Recommended)

If you prefer to install globally (not recommended):

```bash
# Skip the venv step
pip install -r requirements.txt

# Run directly
python main.py --demo -q "laptop"
```

**Drawbacks:**
- May conflict with other Python projects
- Harder to manage dependencies
- Can pollute system Python installation
- Requires sudo/admin on some systems

---

## Troubleshooting

### "python3: command not found"

**On some systems, use `python` instead:**
```bash
python --version
python -m venv venv
```

### "pip: command not found"

**Install pip:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# macOS (with Homebrew)
brew install python3

# Windows: Reinstall Python with pip option checked
```

### Virtual environment not activating on Windows PowerShell

**Error:** "cannot be loaded because running scripts is disabled"

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Dependencies fail to install

**Try upgrading pip first:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "No module named 'venv'"

**Install venv package:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# Then create venv
python3 -m venv venv
```

---

## Virtual Environment Commands Reference

| Action | Linux/Mac | Windows |
|--------|-----------|---------|
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `venv\Scripts\activate` |
| Deactivate | `deactivate` | `deactivate` |
| Delete | `rm -rf venv` | `rmdir /s venv` |

---

## What Gets Installed

The following packages will be installed in your virtual environment:

```
requests>=2.31.0        # HTTP requests for scraping
beautifulsoup4>=4.12.0  # HTML parsing
lxml>=4.9.0            # Fast XML/HTML parser
colorama>=0.4.6        # Colored terminal output
python-dateutil>=2.8.2 # Date/time utilities
```

Total size: ~15-20 MB

---

## Updating Dependencies

If we release updates to dependencies:

```bash
# Activate venv first
source venv/bin/activate  # or Windows equivalent

# Update packages
pip install --upgrade -r requirements.txt
```

---

## Clean Installation

If you need to start fresh:

```bash
# Deactivate if active
deactivate

# Delete virtual environment
rm -rf venv  # Linux/Mac
# or
rmdir /s venv  # Windows

# Recreate from scratch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Production Deployment with Virtual Environment

For production servers:

```bash
# Create venv on production server
python3 -m venv /opt/dealscan/venv

# Activate
source /opt/dealscan/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up systemd service or cron job using the venv python
/opt/dealscan/venv/bin/python /opt/dealscan/main.py --demo -q "laptop"
```

---

## Docker Alternative

If you prefer containerization, here's a basic Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py", "--demo", "-q", "laptop"]
```

Build and run:
```bash
docker build -t dealscan .
docker run dealscan
```

---

## Summary

**Recommended workflow:**

1. ✅ Clone repository
2. ✅ Create virtual environment (`python3 -m venv venv`)
3. ✅ Activate it (`source venv/bin/activate`)
4. ✅ Install dependencies (`pip install -r requirements.txt`)
5. ✅ Run DealScan (`python main.py --demo -q "laptop"`)
6. ✅ Deactivate when done (`deactivate`)

**Always activate the venv before running DealScan!**

---

## Next Steps

After installation:
- Try demo mode: `python main.py --demo -q "gaming laptop"`
- Read [README.md](README.md) for usage details
- See [PROXY_SETUP.md](PROXY_SETUP.md) for production deployment
- Review [COMPLIANCE_GUIDE.md](COMPLIANCE_GUIDE.md) for legal info

Happy deal hunting! 🎯
