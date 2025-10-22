#!/usr/bin/env python3
"""Debug script to check what's happening with DealNews URL."""
import requests

urls_to_test = [
    "https://www.dealnews.com",
    "https://www.dealnews.com/features/Staff-Picks/",
    "https://www.dealnews.com/features/staff-picks/",  # lowercase
    "https://dealnews.com",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for url in urls_to_test:
    print(f"\n{'='*70}")
    print(f"Testing: {url}")
    print('='*70)

    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        print(f"Content Length: {len(response.content)} bytes")
        print(f"Redirects: {len(response.history)} redirect(s)")

        if response.history:
            print("Redirect chain:")
            for i, r in enumerate(response.history, 1):
                print(f"  {i}. {r.status_code} -> {r.url}")
            print(f"  Final: {response.status_code} -> {response.url}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
        print(f"Status Code: {e.response.status_code if e.response else 'N/A'}")
    except Exception as e:
        print(f"Error: {e}")
