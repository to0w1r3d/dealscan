"""Advanced Slickdeals scraper with multiple fallback strategies."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
import time
import random


class SlickdealsAdvancedScraper:
    """
    Advanced Slickdeals scraper with multiple strategies.

    Note: Slickdeals has a 0/10 scraping difficulty but may block datacenter IPs.
    This scraper supports proxy configuration for residential IP access.
    """

    def __init__(self, proxy: Optional[str] = None):
        """
        Initialize scraper.

        Args:
            proxy: Optional proxy URL (e.g., 'http://user:pass@host:port')
        """
        self.base_url = "https://slickdeals.net"
        self.session = requests.Session()

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

    def scrape_deals(self, use_api: bool = False) -> List[Dict]:
        """
        Scrape deals from Slickdeals.

        Args:
            use_api: If True, attempts to use Slickdeals API endpoints

        Returns:
            List of deal dictionaries
        """
        if use_api:
            return self._scrape_via_api()
        else:
            return self._scrape_via_html()

    def _scrape_via_html(self) -> List[Dict]:
        """Scrape via HTML parsing."""
        urls_to_try = [
            f"{self.base_url}/deals/",
            f"{self.base_url}/",
            "https://www.slickdeals.net/deals/",
        ]

        for url in urls_to_try:
            try:
                time.sleep(random.uniform(1, 2))
                response = self.session.get(url, timeout=15)

                if response.status_code == 200:
                    return self._parse_html(response.content)
                elif response.status_code == 403:
                    continue

            except Exception as e:
                continue

        # All attempts failed
        return []

    def _scrape_via_api(self) -> List[Dict]:
        """
        Attempt to scrape via Slickdeals API endpoints.

        Slickdeals may have JSON endpoints for their frontend.
        """
        # These are potential API endpoints that might work
        api_urls = [
            f"{self.base_url}/rest_api/v1/fp",
            f"{self.base_url}/ajax/api/deals",
        ]

        for api_url in api_urls:
            try:
                response = self.session.get(api_url, timeout=15)
                if response.status_code == 200:
                    return self._parse_api_response(response.json())
            except:
                continue

        return []

    def _parse_html(self, content: bytes) -> List[Dict]:
        """Parse HTML content for deals."""
        soup = BeautifulSoup(content, 'lxml')
        deals = []

        # Multiple selector strategies
        selectors = [
            'li.fpGrid',
            'article[class*="deal"]',
            'div[data-id]',
        ]

        for selector in selectors:
            cards = soup.select(selector)
            if cards:
                for card in cards:
                    deal = self._parse_deal_card(card)
                    if deal:
                        deals.append(deal)
                break

        return deals

    def _parse_deal_card(self, card) -> Optional[Dict]:
        """Parse individual deal card."""
        try:
            # Title and link
            title_elem = card.select_one('a[class*="dealLink"], a[class*="title"]')
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"

            # Price
            price_elem = card.select_one('[class*="price"], .itemPrice')
            price = price_elem.get_text(strip=True) if price_elem else "N/A"

            # Store
            store_elem = card.select_one('[class*="store"], .blueprint')
            store = store_elem.get_text(strip=True) if store_elem else "Unknown"

            # Score
            score_elem = card.select_one('[class*="score"], .itemScore')
            score = self._extract_number(score_elem.get_text(strip=True)) if score_elem else 0

            # Comments
            comment_elem = card.select_one('[class*="comment"]')
            comments = self._extract_number(comment_elem.get_text(strip=True)) if comment_elem else 0

            return {
                'title': title,
                'price': price,
                'store': store,
                'link': link,
                'score': score,
                'comments': comments,
                'source': 'Slickdeals',
                'timestamp': datetime.now()
            }
        except:
            return None

    def _parse_api_response(self, data: dict) -> List[Dict]:
        """Parse API JSON response."""
        # This would depend on the actual API structure
        # Placeholder for future implementation
        return []

    def _extract_number(self, text: str) -> int:
        """Extract number from text."""
        if not text:
            return 0
        match = re.search(r'\d+', text.replace(',', ''))
        return int(match.group()) if match else 0
