"""Slickdeals frontpage scraper."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
import time
import random


class SlickdealsScraper:
    """Scraper for Slickdeals frontpage deals."""

    def __init__(self):
        self.base_url = "https://slickdeals.net"
        self.frontpage_url = f"{self.base_url}/deals/"
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
        Scrape deals from Slickdeals frontpage.

        Returns:
            List of deal dictionaries with title, price, link, score, etc.
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

            response = self.session.get(self.frontpage_url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')
            deals = []

            # Find deal cards on the frontpage
            deal_cards = soup.find_all('li', class_='fpGrid')

            for card in deal_cards:
                try:
                    deal = self._parse_deal_card(card)
                    if deal:
                        deals.append(deal)
                except Exception as e:
                    # Skip individual deal parsing errors
                    continue

            return deals

        except Exception as e:
            print(f"Error scraping Slickdeals: {e}")
            return []

    def _parse_deal_card(self, card) -> Optional[Dict]:
        """Parse a single deal card from Slickdeals."""
        try:
            # Extract title
            title_elem = card.find('a', class_='bp-p-dealLink')
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"

            # Extract price
            price_elem = card.find('span', class_='itemPrice')
            price = price_elem.get_text(strip=True) if price_elem else "N/A"

            # Extract store/merchant
            store_elem = card.find('span', class_='blueprint')
            if not store_elem:
                store_elem = card.find('button', class_='bp-p-storeBtn')
            store = store_elem.get_text(strip=True) if store_elem else "Unknown"

            # Extract score/votes
            score_elem = card.find('span', class_='itemScore')
            score_text = score_elem.get_text(strip=True) if score_elem else "0"
            score = self._extract_number(score_text)

            # Extract comment count
            comment_elem = card.find('span', class_='bp-p-discussionLink_text')
            comment_text = comment_elem.get_text(strip=True) if comment_elem else "0"
            comments = self._extract_number(comment_text)

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

        except Exception as e:
            return None

    def _extract_number(self, text: str) -> int:
        """Extract numeric value from text."""
        if not text:
            return 0
        # Extract first number found in string
        match = re.search(r'\d+', text)
        return int(match.group()) if match else 0
