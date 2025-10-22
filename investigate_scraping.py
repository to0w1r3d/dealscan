#!/usr/bin/env python3
"""Test different scraping approaches for Slickdeals."""
import requests
from bs4 import BeautifulSoup
import time

print("="*70)
print("Slickdeals Scraping Investigation")
print("Analysis shows: 0/10 difficulty (Easy)")
print("="*70)

# Test 1: Minimal approach
print("\n[Test 1] Minimal request (no headers)")
try:
    response = requests.get("https://slickdeals.net", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.content)}")
    if response.status_code == 200:
        print("✓ SUCCESS with minimal approach!")
        print(f"First 200 chars: {response.text[:200]}")
except Exception as e:
    print(f"✗ FAILED: {e}")

time.sleep(2)

# Test 2: Simple User-Agent only
print("\n[Test 2] Simple User-Agent only")
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get("https://slickdeals.net", headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.content)}")
    if response.status_code == 200:
        print("✓ SUCCESS with simple User-Agent!")
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"Page title: {soup.title.string if soup.title else 'No title'}")
except Exception as e:
    print(f"✗ FAILED: {e}")

time.sleep(2)

# Test 3: Try different Slickdeals URLs
urls_to_test = [
    "https://slickdeals.net",
    "https://www.slickdeals.net",
    "https://slickdeals.net/deals/",
    "https://www.slickdeals.net/deals/",
]

print("\n[Test 3] Testing different URLs")
for url in urls_to_test:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"\n{url}")
        print(f"  Status: {response.status_code}")
        print(f"  Final URL: {response.url}")
        print(f"  Size: {len(response.content)} bytes")

        if response.status_code == 200:
            print(f"  ✓ SUCCESS")
            # Try to find deal elements
            soup = BeautifulSoup(response.content, 'html.parser')

            # Look for common deal-related classes
            potential_selectors = [
                'div[class*="deal"]',
                'article',
                'li[class*="fp"]',
                'div[class*="grid"]',
                'a[href*="/f/"]',
            ]

            for selector in potential_selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"    Found {len(elements)} elements with: {selector}")
        else:
            print(f"  ✗ HTTP {response.status_code}")

        time.sleep(2)
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

# Test 4: Check robots.txt
print("\n[Test 4] Checking robots.txt")
try:
    response = requests.get("https://slickdeals.net/robots.txt", timeout=10)
    if response.status_code == 200:
        print("✓ robots.txt accessible")
        print("First 500 chars:")
        print(response.text[:500])
except Exception as e:
    print(f"✗ FAILED: {e}")

print("\n" + "="*70)
print("Investigation Complete")
print("="*70)
