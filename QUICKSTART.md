# DealScan Quick Start Guide

Get up and running with DealScan in 5 minutes!

---

## 🚀 First Time Setup

```bash
# 1. Clone the repository
git clone https://github.com/to0w1r3d/dealscan.git
cd dealscan

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate        # Linux/Mac
# or: venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test it works
python main.py --demo -q "laptop"
```

**Expected output:** Colorful list of laptop deals ranked by relevance! 🎉

---

## 💻 Daily Usage

### Every time you use DealScan:

```bash
# 1. Navigate to project
cd dealscan

# 2. Activate virtual environment
source venv/bin/activate        # Linux/Mac
# or: venv\Scripts\activate     # Windows

# 3. Run DealScan
python main.py --demo -q "your search"

# 4. When done
deactivate
```

---

## 📋 Common Commands

### Demo Mode (Works Immediately)

```bash
# Search for laptops
python main.py --demo -q "laptop"

# Search for gaming gear
python main.py --demo -q "gaming"

# Search for headphones
python main.py --demo -q "wireless headphones"

# Interactive mode (prompts for search)
python main.py --demo
```

### Live Mode (Requires Residential IP)

```bash
# Will show 403 errors from datacenter IP
python main.py -q "laptop"

# Works from home WiFi (residential IP)
python main.py -q "gaming laptop"
```

### Testing & Validation

```bash
# Run production test suite
python production_test.py

# Test both scrapers
python test_both_sites.py

# Check syntax
python -m py_compile main.py
```

---

## 🔧 Virtual Environment Cheat Sheet

| Task | Command (Linux/Mac) | Command (Windows) |
|------|---------------------|-------------------|
| **Create** | `python3 -m venv venv` | `python -m venv venv` |
| **Activate** | `source venv/bin/activate` | `venv\Scripts\activate` |
| **Deactivate** | `deactivate` | `deactivate` |
| **Delete** | `rm -rf venv` | `rmdir /s venv` |
| **Check if active** | `which python` (should show venv path) | `where python` |

### How to tell if venv is active:

Your prompt will show `(venv)` at the beginning:
```
(venv) user@computer:~/dealscan$
```

---

## 🌐 Production Deployment

### Home Computer (Free)

```bash
# On your home computer (residential IP)
cd dealscan
source venv/bin/activate
python main.py -q "laptop"  # Should work!
```

### With Residential Proxy (~$75/month)

```bash
# Set proxy
export RESIDENTIAL_PROXY="http://user:pass@proxy.com:port"

# Use advanced scrapers
source venv/bin/activate
python
```

```python
from scrapers.slickdeals_advanced import SlickdealsAdvancedScraper
import os

scraper = SlickdealsAdvancedScraper(proxy=os.getenv('RESIDENTIAL_PROXY'))
deals = scraper.scrape_deals()
```

---

## 🐛 Troubleshooting

### "Command not found: python3"

Try `python` instead:
```bash
python -m venv venv
```

### "No module named 'requests'"

Make sure venv is activated (you should see `(venv)` in prompt):
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "403 Forbidden" errors

This is **expected** from datacenter IPs. Both sites work fine but block datacenter IPs via Cloudflare.

**Solutions:**
- ✅ Use `--demo` mode for testing
- ✅ Run from home computer (residential IP)
- ✅ Use residential proxy service

### Virtual environment not activating

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| [README.md](README.md) | Full project documentation |
| [INSTALL.md](INSTALL.md) | Detailed installation guide |
| [PROXY_SETUP.md](PROXY_SETUP.md) | Residential proxy configuration |
| [COMPLIANCE_GUIDE.md](COMPLIANCE_GUIDE.md) | Legal & ethical guidelines |
| [SCRAPING_ANALYSIS.md](SCRAPING_ANALYSIS.md) | Technical analysis |
| [PRODUCTION_TEST_REPORT_FINAL.md](PRODUCTION_TEST_REPORT_FINAL.md) | Test results |

---

## 🎯 Example Workflow

**Typical usage session:**

```bash
# Morning: Start work
cd ~/dealscan
source venv/bin/activate

# Test with demo mode
python main.py --demo -q "laptop deals"

# Try different queries
python main.py --demo -q "gaming monitor"
python main.py --demo -q "mechanical keyboard"

# Run tests
python production_test.py

# Evening: Clean up
deactivate
```

---

## ⚡ One-Liner Tests

```bash
# Quick test (from project root)
source venv/bin/activate && python main.py --demo -q "laptop" && deactivate

# Run all tests
source venv/bin/activate && python production_test.py && deactivate
```

---

## 🎨 Sample Output

When working correctly, you'll see:

```
================================================================================
  DealScan - Product Deal Scraper
  Search Slickdeals & DealNews for the best product deals
================================================================================

Running in DEMO mode with sample data

Searching for: laptop

[DEMO MODE] Using sample deal data...
Loaded 18 sample deals

Matching deals to search query...
Ranking deals...

Found 18 deals matching 'laptop':

================================================================================

#1 - Score: 88.3
  Dell XPS 13 Laptop - Intel i7, 16GB RAM, 512GB SSD
  Price: $899.99
  Store: Dell
  Source: Slickdeals | Upvotes: 189 | Comments: 93
  Link: https://slickdeals.net/example

#2 - Score: 86.5
  Apple MacBook Air M2 13" Laptop - 8GB RAM, 256GB SSD
  ...
```

---

## 🚦 Status Indicators

- ✅ **Green text** = Successful operation
- ❌ **Red text** = Error (usually 403 from datacenter IP)
- ⚠️ **Yellow text** = Warning or info
- 🔵 **Blue text** = Links

---

## 📞 Getting Help

- **Installation issues:** See [INSTALL.md](INSTALL.md)
- **Proxy setup:** See [PROXY_SETUP.md](PROXY_SETUP.md)
- **403 errors:** Expected from datacenter IPs, use `--demo` or residential IP
- **General questions:** Check [README.md](README.md)

---

## 🎓 Key Concepts

1. **Virtual Environment** - Isolated Python environment (always activate before use)
2. **Demo Mode** - Uses sample data, works immediately
3. **Live Mode** - Scrapes real sites, needs residential IP
4. **Residential IP** - Home internet IP (not blocked)
5. **Datacenter IP** - Server IP (blocked by Cloudflare)
6. **Crawl-Delay** - DealNews requires 2.0s delay (automatic)

---

## ✨ Best Practices

1. ✅ **Always use virtual environment**
2. ✅ **Use demo mode for testing**
3. ✅ **Activate venv before running commands**
4. ✅ **Deactivate when done**
5. ✅ **Never commit venv/ to git** (already in .gitignore)

---

## 🎉 You're Ready!

That's it! You now know how to:
- ✅ Set up and use virtual environments
- ✅ Run DealScan in demo mode
- ✅ Test the application
- ✅ Troubleshoot common issues

**Start searching for deals:**
```bash
source venv/bin/activate
python main.py --demo -q "gaming laptop"
```

Happy deal hunting! 🎯
