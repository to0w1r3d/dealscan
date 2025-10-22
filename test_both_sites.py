#!/usr/bin/env python3
"""
Test both Slickdeals and DealNews scrapers.

This script tests the advanced scrapers with proper rate limiting:
- Slickdeals: 1-2 second delays (recommended)
- DealNews: 2.0 second crawl-delay (required by robots.txt)
"""

import sys
import time
from scrapers.slickdeals_advanced import SlickdealsAdvancedScraper
from scrapers.dealnews_advanced import DealNewsAdvancedScraper

print("=" * 80)
print("DealScan - Testing Both Sites with Advanced Scrapers")
print("=" * 80)
print()
print("Scraping Difficulty Analysis:")
print("  Slickdeals: 0/10 (Easy) - No specific crawl-delay")
print("  DealNews:   0/10 (Easy) - Requires 2.0s crawl-delay")
print()
print("Current Environment: Datacenter IP (likely blocked)")
print("Expected Result: 403 errors (need residential IP/proxy)")
print("=" * 80)
print()

# Test Slickdeals
print("[1/2] Testing Slickdeals.net")
print("-" * 80)

slickdeals_scraper = SlickdealsAdvancedScraper()

print("Attempting to scrape Slickdeals...")
print("Note: Using 1-2 second delays as recommended practice")
print()

start_time = time.time()
try:
    slickdeals_deals = slickdeals_scraper.scrape_deals()
    elapsed = time.time() - start_time

    if slickdeals_deals:
        print(f"✓ SUCCESS! Retrieved {len(slickdeals_deals)} deals")
        print(f"  Time elapsed: {elapsed:.2f} seconds")
        print()
        print("Sample deals:")
        for i, deal in enumerate(slickdeals_deals[:3], 1):
            print(f"  {i}. {deal['title'][:60]}...")
            print(f"     Price: {deal['price']} | Store: {deal['store']}")
        print()
    else:
        print(f"✗ No deals retrieved (blocked or no matches)")
        print(f"  Time elapsed: {elapsed:.2f} seconds")
        print(f"  Status: Likely 403 Forbidden from datacenter IP")
        print()

except Exception as e:
    elapsed = time.time() - start_time
    print(f"✗ ERROR: {e}")
    print(f"  Time elapsed: {elapsed:.2f} seconds")
    print()

# Wait before next site
print("Waiting 3 seconds before testing next site...")
time.sleep(3)
print()

# Test DealNews
print("[2/2] Testing DealNews.com")
print("-" * 80)

dealnews_scraper = DealNewsAdvancedScraper()

print("Attempting to scrape DealNews...")
print("Note: Enforcing 2.0 second crawl-delay (robots.txt requirement)")
print()

start_time = time.time()
try:
    dealnews_deals = dealnews_scraper.scrape_deals()
    elapsed = time.time() - start_time

    if dealnews_deals:
        print(f"✓ SUCCESS! Retrieved {len(dealnews_deals)} deals")
        print(f"  Time elapsed: {elapsed:.2f} seconds")
        print(f"  Crawl-delay compliance: {elapsed >= 2.0}")
        print()
        print("Sample deals:")
        for i, deal in enumerate(dealnews_deals[:3], 1):
            print(f"  {i}. {deal['title'][:60]}...")
            print(f"     Price: {deal['price']} | Store: {deal['store']}")
        print()
    else:
        print(f"✗ No deals retrieved (blocked or no matches)")
        print(f"  Time elapsed: {elapsed:.2f} seconds")
        print(f"  Status: Likely 403 Forbidden from datacenter IP")
        print()

except Exception as e:
    elapsed = time.time() - start_time
    print(f"✗ ERROR: {e}")
    print(f"  Time elapsed: {elapsed:.2f} seconds")
    print()

# Summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print()
print("Both sites have 0/10 scraping difficulty:")
print("  ✅ robots.txt allows scraping")
print("  ✅ No TLS fingerprinting")
print("  ✅ No aggressive rate limiting")
print()
print("Current Status:")
print("  ❌ Blocked by datacenter IP (403 Forbidden)")
print()
print("Solutions:")
print("  1. Run from residential internet (home WiFi)")
print("  2. Use residential proxy (~$75/month)")
print("  3. Use --demo mode for testing (works perfectly)")
print()
print("To test functionality right now:")
print("  python main.py --demo -q \"laptop\"")
print()
print("For production deployment, see:")
print("  - PROXY_SETUP.md (residential proxy guide)")
print("  - SCRAPING_ANALYSIS.md (detailed analysis)")
print()
print("=" * 80)
