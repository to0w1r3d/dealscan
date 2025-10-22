"""Advanced DealNews scraper with robots.txt compliance."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
import time
import random


class DealNewsAdvancedScraper:
    """
    Advanced DealNews scraper with robots.txt compliance.

    DealNews has 0/10 scraping difficulty:
    - robots.txt allows scraping
    - Requires 2.0 second crawl-delay (MUST respect this)
    - No TLS fingerprinting
    - No aggressive rate limiting
    """

    # IMPORTANT: robots.txt specifies crawl-delay: 2.0
    CRAWL_DELAY = 2.0

    def __init__(self, proxy: Optional[str] = None):
        """
        Initialize scraper.

        Args:
            proxy: Optional proxy URL (e.g., 'http://user:pass@host:port')
        """
        self.base_url = "https://www.dealnews.com"
        self.session = requests.Session()
        self.last_request_time = 0

        # Standard browser headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)

        # Configure proxy if provided
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }

    def _respect_crawl_delay(self):
        """Enforce crawl-delay as specified in robots.txt."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.CRAWL_DELAY:
            delay = self.CRAWL_DELAY - elapsed
            time.sleep(delay)
        self.last_request_time = time.time()

    def scrape_deals(self) -> List[Dict]:
        """
        Scrape deals from DealNews staff picks.

        Respects robots.txt crawl-delay of 2.0 seconds.

        Returns:
            List of deal dictionaries
        """
        # URLs to try
        urls_to_try = [
            f"{self.base_url}/features/Staff-Picks/",
            f"{self.base_url}/",
        ]

        for url in urls_to_try:
            try:
                # IMPORTANT: Respect crawl-delay
                self._respect_crawl_delay()

                response = self.session.get(url, timeout=15)

                if response.status_code == 200:
                    return self._parse_html(response.content)
                elif response.status_code == 403:
                    continue

            except Exception as e:
                continue

        return []

    def _parse_html(self, content: bytes) -> List[Dict]:
        """Parse HTML content for deals."""
        soup = BeautifulSoup(content, 'lxml')
        deals = []

        # Multiple selector strategies for DealNews
        selectors = [
            'article[class*="deal"]',
            'div[class*="deal-item"]',
            'div[class*="story"]',
            'article',
        ]

        for selector in selectors:
            items = soup.select(selector)
            if items:
                for item in items:
                    deal = self._parse_deal_item(item)
                    if deal:
                        deals.append(deal)
                if deals:  # If we found deals with this selector, stop trying
                    break

        return deals

    def _parse_deal_item(self, item) -> Optional[Dict]:
        """Parse individual deal item."""
        try:
            # Title and link - try multiple selectors
            title_elem = (
                item.select_one('a[class*="title"]') or
                item.select_one('a[class*="headline"]') or
                item.select_one('h2 a') or
                item.select_one('h3 a') or
                item.find('a')
            )

            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            if not title or len(title) < 10:  # Skip if title too short
                return None

            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"

            # Price - try multiple selectors
            price_elem = (
                item.select_one('[class*="price"]') or
                item.select_one('.price') or
                item.select_one('span[class*="price"]')
            )

            if price_elem:
                price = price_elem.get_text(strip=True)
            else:
                # Look for price pattern in text
                text = item.get_text()
                price_match = re.search(r'\$[\d,]+\.?\d*', text)
                price = price_match.group() if price_match else "N/A"

            # Store/merchant
            store_elem = (
                item.select_one('[class*="store"]') or
                item.select_one('[class*="merchant"]') or
                item.select_one('[class*="vendor"]')
            )
            store = store_elem.get_text(strip=True) if store_elem else "Unknown"

            # Category
            category_elem = item.select_one('[class*="category"]')
            category = category_elem.get_text(strip=True) if category_elem else ""

            # DealNews staff picks don't have community scores
            # Give them a standard high score since they're curated
            return {
                'title': title,
                'price': price,
                'store': store,
                'link': link,
                'score': 100,  # Staff picks are pre-vetted
                'comments': 0,
                'category': category,
                'source': 'DealNews',
                'timestamp': datetime.now()
            }

        except Exception as e:
            return None

    def scrape_multiple_pages(self, max_pages: int = 3) -> List[Dict]:
        """
        Scrape multiple pages of deals.

        Args:
            max_pages: Maximum number of pages to scrape

        Returns:
            Combined list of deals from all pages
        """
        all_deals = []

        for page in range(1, max_pages + 1):
            # Respect crawl-delay between page requests
            self._respect_crawl_delay()

            url = f"{self.base_url}/features/Staff-Picks/?page={page}"

            try:
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    deals = self._parse_html(response.content)
                    all_deals.extend(deals)

                    if not deals:  # No more deals found
                        break
                else:
                    break

            except Exception as e:
                break

        return all_deals
