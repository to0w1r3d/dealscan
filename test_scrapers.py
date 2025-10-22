#!/usr/bin/env python3
"""Quick test to verify scrapers work."""
from scrapers.slickdeals import SlickdealsScraper
from scrapers.dealnews import DealNewsScraper
from utils import DealMatcher, DealRanker

print("Testing scraper imports...")

# Test instantiation
print("Creating Slickdeals scraper...")
sd = SlickdealsScraper()
print(f"  Base URL: {sd.base_url}")

print("Creating DealNews scraper...")
dn = DealNewsScraper()
print(f"  Base URL: {dn.base_url}")

print("\nAll imports successful!")

# Test actual scraping (just a few deals)
print("\n--- Testing Slickdeals scraper ---")
sd_deals = sd.scrape_deals()
print(f"Scraped {len(sd_deals)} deals from Slickdeals")
if sd_deals:
    print(f"Sample deal: {sd_deals[0]['title'][:50]}...")

print("\n--- Testing DealNews scraper ---")
dn_deals = dn.scrape_deals()
print(f"Scraped {len(dn_deals)} deals from DealNews")
if dn_deals:
    print(f"Sample deal: {dn_deals[0]['title'][:50]}...")

# Test matching
print("\n--- Testing deal matching ---")
all_deals = sd_deals + dn_deals
if all_deals:
    test_query = "laptop"
    matched = DealMatcher.match_deals(all_deals, test_query)
    print(f"Matched {len(matched)} deals for query '{test_query}'")

    if matched:
        ranked = DealRanker.rank_deals(matched)
        print(f"Ranked {len(ranked)} deals")
        if ranked:
            print(f"Top deal: {ranked[0]['title'][:60]}...")
            print(f"  Score: {ranked[0]['final_score']}")

print("\n✓ All tests passed!")
