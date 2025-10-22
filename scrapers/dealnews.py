"""DealNews staff picks scraper."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
import time
import random


class DealNewsScraper:
    """Scraper for DealNews staff picks."""

    def __init__(self):
        self.base_url = "https://www.dealnews.com"
        self.staff_picks_url = f"{self.base_url}/features/Staff-Picks/"
        self.session = requests.Session()
        self.headers = {
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
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
        self.session.headers.update(self.headers)

    def scrape_deals(self) -> List[Dict]:
        """
        Scrape deals from DealNews staff picks.

        Returns:
            List of deal dictionaries with title, price, link, etc.
        """
        try:
            # Add random delay to seem more human-like
            time.sleep(random.uniform(0.5, 1.5))

            # Try the homepage first to get cookies
            try:
                self.session.get(self.base_url, timeout=10)
                time.sleep(random.uniform(0.5, 1.0))
            except:
                pass

            response = self.session.get(self.staff_picks_url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')
            deals = []

            # Find deal items on the staff picks page
            # DealNews uses article tags or deal-item divs
            deal_items = soup.find_all('article', class_=re.compile(r'deal'))

            if not deal_items:
                # Try alternative selectors
                deal_items = soup.find_all('div', class_=re.compile(r'deal-item|story'))

            for item in deal_items:
                try:
                    deal = self._parse_deal_item(item)
                    if deal:
                        deals.append(deal)
                except Exception as e:
                    continue

            return deals

        except Exception as e:
            print(f"Error scraping DealNews: {e}")
            return []

    def _parse_deal_item(self, item) -> Optional[Dict]:
        """Parse a single deal item from DealNews."""
        try:
            # Extract title
            title_elem = item.find('a', class_=re.compile(r'title|headline'))
            if not title_elem:
                # Try finding any link with substantial text
                title_elem = item.find('a')

            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"

            # Extract price
            price_elem = item.find(['span', 'div'], class_=re.compile(r'price'))
            if not price_elem:
                # Look for price pattern in text
                price_text = item.get_text()
                price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                price = price_match.group() if price_match else "N/A"
            else:
                price = price_elem.get_text(strip=True)

            # Extract store/merchant
            store_elem = item.find(['span', 'div'], class_=re.compile(r'store|merchant|vendor'))
            store = store_elem.get_text(strip=True) if store_elem else "Unknown"

            # Extract category
            category_elem = item.find(['span', 'div'], class_=re.compile(r'category'))
            category = category_elem.get_text(strip=True) if category_elem else ""

            # DealNews doesn't have scores like Slickdeals, so we'll use 0
            # and rely more on the staff pick designation

            return {
                'title': title,
                'price': price,
                'store': store,
                'link': link,
                'score': 100,  # Staff picks are pre-vetted, give them a boost
                'comments': 0,
                'category': category,
                'source': 'DealNews',
                'timestamp': datetime.now()
            }

        except Exception as e:
            return None
