# Using DealScan with Residential Proxies

Since Slickdeals blocks datacenter IPs but has a 0/10 scraping difficulty from residential IPs, using a residential proxy is the recommended solution for production deployments.

## Prerequisites

Before setting up proxies, ensure DealScan is installed in a virtual environment:

```bash
# Clone and setup (if not done already)
git clone https://github.com/to0w1r3d/dealscan.git
cd dealscan

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Quick Start with Proxy

### Method 1: Environment Variable

```bash
# Set proxy in environment
export RESIDENTIAL_PROXY="http://username:password@proxy.provider.com:port"

# Run with proxy support (future implementation)
python main.py -q "laptop"
```

### Method 2: Use Advanced Scraper Directly

```python
from scrapers.slickdeals_advanced import SlickdealsAdvancedScraper

# Initialize with proxy
scraper = SlickdealsAdvancedScraper(
    proxy="http://username:password@proxy.provider.com:port"
)

# Scrape deals
deals = scraper.scrape_deals()

for deal in deals:
    print(f"{deal['title']} - {deal['price']}")
```

## Residential Proxy Providers

### Recommended Providers

#### 1. Bright Data (Premium, Most Reliable)
- **Website**: https://brightdata.com
- **Pricing**: ~$500/month (entry plan)
- **Features**:
  - Largest residential proxy network
  - 99.99% uptime
  - Pay-per-GB pricing
  - Automatic rotation
- **Best for**: Enterprise production use

#### 2. Smartproxy (Good Balance)
- **Website**: https://smartproxy.com
- **Pricing**: ~$75/month (8GB)
- **Features**:
  - 40M+ residential IPs
  - Easy dashboard
  - 24/7 support
- **Best for**: Small to medium projects

#### 3. Oxylabs (Enterprise)
- **Website**: https://oxylabs.io
- **Pricing**: Custom (usually $600+/month)
- **Features**:
  - Premium quality IPs
  - Dedicated account manager
  - High success rate
- **Best for**: Large-scale operations

#### 4. GeoSurf (Budget-Friendly)
- **Website**: https://www.geosurf.com
- **Pricing**: ~$50/month (starter)
- **Features**:
  - Good for beginners
  - Simple API
  - City-level targeting
- **Best for**: Development/testing

### Free Alternatives (Limited)

#### ProxyMesh
- **Website**: https://proxymesh.com
- **Pricing**: Free tier available
- **Limitations**: Limited bandwidth, may not work for all sites

#### ScraperAPI Free Tier
- **Website**: https://www.scraperapi.com
- **Pricing**: 1,000 free API calls/month
- **Features**: Handles proxies and browsers automatically

## Configuration Examples

### Format

Proxy URLs follow this format:
```
http://username:password@host:port
https://username:password@host:port
socks5://username:password@host:port
```

### Example Configuration

```python
# config.py
import os

PROXY_CONFIG = {
    'residential': os.getenv('RESIDENTIAL_PROXY', None),
    'datacenter': os.getenv('DATACENTER_PROXY', None),
    'rotate': True,  # Rotate IPs automatically
    'timeout': 15,   # Request timeout in seconds
}

# Usage
from scrapers.slickdeals_advanced import SlickdealsAdvancedScraper

scraper = SlickdealsAdvancedScraper(
    proxy=PROXY_CONFIG['residential']
)
```

## Testing Your Proxy

Before scraping, verify your proxy works:

```python
import requests

proxy = "http://username:password@proxy.provider.com:port"

proxies = {
    'http': proxy,
    'https': proxy
}

# Test the proxy
try:
    response = requests.get(
        'https://slickdeals.net',
        proxies=proxies,
        timeout=15
    )

    if response.status_code == 200:
        print("✓ Proxy working! Status: 200")
        print(f"  Content length: {len(response.content)} bytes")
    else:
        print(f"✗ Failed with status: {response.status_code}")

except Exception as e:
    print(f"✗ Proxy error: {e}")
```

## Best Practices

### 1. Respect Rate Limits

Even with working proxies, respect the site:

```python
import time
import random

# Between requests
time.sleep(random.uniform(2, 5))

# Between sessions
time.sleep(random.uniform(10, 20))
```

### 2. Rotate User Agents

```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...',
]

headers = {
    'User-Agent': random.choice(user_agents)
}
```

### 3. Handle Failures Gracefully

```python
max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        deals = scraper.scrape_deals()
        if deals:
            break
    except Exception as e:
        retry_count += 1
        time.sleep(retry_count * 2)  # Exponential backoff
```

### 4. Monitor Success Rate

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

successful_requests = 0
failed_requests = 0

try:
    deals = scraper.scrape_deals()
    successful_requests += 1
    logger.info(f"Success! Got {len(deals)} deals")
except:
    failed_requests += 1
    logger.error("Request failed")

success_rate = successful_requests / (successful_requests + failed_requests)
logger.info(f"Success rate: {success_rate:.1%}")
```

## Cost Estimation

### Bandwidth Usage

- Average page size: ~2-3 MB (HTML + resources)
- Deals page only (HTML): ~200-500 KB
- Typical monthly usage (1 request/5 min): ~10-15 GB

### Pricing Examples

| Requests/Day | Monthly GB | Smartproxy | Bright Data |
|-------------|-----------|------------|-------------|
| 288 (5 min) | ~15 GB    | $75        | ~$750       |
| 1,440 (1 min) | ~75 GB  | $250       | ~$3,750     |
| 2,880 (30 sec) | ~150 GB | $500      | ~$7,500     |

## Alternative: Run from Home

If proxies are too expensive, run the scraper from your home computer:

```bash
# Clone on your home PC
git clone https://github.com/to0w1r3d/dealscan.git
cd dealscan

# Install dependencies
pip install -r requirements.txt

# Run without proxy (uses your residential IP)
python main.py -q "laptop"
```

This works because home IPs are residential and not blocked.

## Troubleshooting

### Proxy Still Returns 403

1. **Check proxy type**: Must be residential, not datacenter
2. **Verify credentials**: Username/password correct
3. **Test proxy**: Use the test script above
4. **Try different provider**: Some proxies are better for specific sites

### Slow Response Times

1. **Choose closer proxy location**: Use US proxies for US sites
2. **Upgrade plan**: Higher tiers often have better performance
3. **Reduce concurrent requests**: Don't overwhelm the proxy

### High Cost

1. **Cache results**: Don't re-scrape frequently
2. **Scrape less often**: Update every 15-30 minutes instead of every minute
3. **Use demo mode for development**: Only use live scraping in production

## Recommended Setup

For production use:

```python
# production_config.py
import os
from scrapers.slickdeals_advanced import SlickdealsAdvancedScraper
import time
import random

class ProductionScraper:
    def __init__(self):
        self.proxy = os.getenv('RESIDENTIAL_PROXY')
        if not self.proxy:
            raise ValueError("RESIDENTIAL_PROXY environment variable required")

        self.scraper = SlickdealsAdvancedScraper(proxy=self.proxy)
        self.last_request = 0
        self.min_delay = 5  # Minimum seconds between requests

    def scrape(self):
        # Rate limiting
        elapsed = time.time() - self.last_request
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)

        # Scrape with retry logic
        for attempt in range(3):
            try:
                deals = self.scraper.scrape_deals()
                self.last_request = time.time()
                return deals
            except Exception as e:
                if attempt < 2:
                    time.sleep(random.uniform(2, 5))
                    continue
                raise e

# Usage
scraper = ProductionScraper()
deals = scraper.scrape()
```

## Summary

**For testing/development:**
- Use `--demo` mode (free, instant)

**For production:**
- Residential proxy (recommended): $75-500/month
- Run from home computer (free but less reliable)
- Use ScraperAPI free tier (limited but managed)

The scraping itself is easy (0/10 difficulty) - you just need the right IP address.
