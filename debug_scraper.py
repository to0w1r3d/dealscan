#!/usr/bin/env python3
"""Debug script to test scraping capabilities."""
import requests
import time

def test_url(url, name):
    """Test if we can access a URL."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print('='*60)

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'DNT': '1',
        'Referer': 'https://www.google.com/'
    }

    try:
        response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        print(f"Response Size: {len(response.content)} bytes")
        print(f"Headers: {dict(list(response.headers.items())[:5])}")

        if response.status_code == 200:
            print(f"✓ SUCCESS - Page accessible")
            print(f"First 500 chars of content:")
            print(response.text[:500])
            return True
        else:
            print(f"✗ FAILED - HTTP {response.status_code}")
            print(f"Response text (first 500 chars):")
            print(response.text[:500])
            return False

    except requests.exceptions.RequestException as e:
        print(f"✗ ERROR: {e}")
        return False

# Test sites
print("\nDeal Scraper Diagnostic Test")
print("="*60)

results = []

# Test Slickdeals
results.append(("Slickdeals Homepage", test_url("https://slickdeals.net", "Slickdeals Homepage")))
time.sleep(2)
results.append(("Slickdeals Deals", test_url("https://slickdeals.net/deals/", "Slickdeals Deals Page")))
time.sleep(2)

# Test DealNews
results.append(("DealNews Homepage", test_url("https://www.dealnews.com", "DealNews Homepage")))
time.sleep(2)
results.append(("DealNews Staff Picks", test_url("https://www.dealnews.com/features/Staff-Picks/", "DealNews Staff Picks")))

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for name, success in results:
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {name}")

print("\nConclusion:")
if any(r[1] for r in results):
    print("At least some URLs are accessible. Scraping may be possible.")
else:
    print("All URLs blocked. These sites have strong anti-bot protection.")
    print("Recommendation: Use --demo mode for testing functionality.")
