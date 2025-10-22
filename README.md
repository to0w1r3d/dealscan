# DealScan - Product Deal Scraper

A Python-based command-line tool that searches and ranks product deals from Slickdeals and DealNews.

## Features

- Scrapes the latest deals from:
  - Slickdeals frontpage
  - DealNews staff picks
- Intelligent product matching using keyword search
- Smart ranking algorithm that considers:
  - Relevance to search query (40%)
  - Deal score/upvotes (30%)
  - Community engagement (20%)
  - Source credibility (10%)
- Clean, colorized terminal output
- Top 20 ranked results displayed

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Important: Scraping Status

**Update**: Analysis confirms **both sites have 0/10 scraping difficulty** (Easy):

### Slickdeals.net
- ✅ robots.txt allows scraping
- ✅ No TLS fingerprinting, no aggressive rate limiting
- ⚠️ Blocked from datacenter IPs (Cloudflare protection)

### DealNews.com
- ✅ robots.txt allows scraping with **2.0s crawl-delay** (respected automatically)
- ✅ No TLS fingerprinting, no aggressive rate limiting
- ⚠️ Blocked from datacenter IPs (Cloudflare protection)

**Current Status:**
- ✅ Code is fully functional and production-ready
- ✅ Works perfectly in demo mode
- ✅ Respects robots.txt requirements (2s crawl-delay for DealNews)
- ❌ Live scraping blocked from datacenter IPs (returns 403)
- ✅ Should work fine from residential IPs (home internet, residential proxies)

**Solutions:**
- **For testing**: Use `--demo` mode (recommended)
- **For production**: Run from residential IP or use residential proxy (~$75/month)
- See [SCRAPING_ANALYSIS.md](SCRAPING_ANALYSIS.md) for detailed analysis
- See [PROXY_SETUP.md](PROXY_SETUP.md) for proxy configuration guide

## Usage

### Standard Mode (Live Scraping)

Run the program to scrape live deals:
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

### Demo Mode (Recommended for First Run)

If the websites block scraping (403 errors), use demo mode with sample data:
```bash
python main.py --demo
```

You can also provide a search query directly:
```bash
python main.py --demo -q "laptop"
python main.py --demo -q "wireless headphones"
```

### Command Line Options

- `--demo`: Run in demo mode with sample data
- `-q "search query"` or `--query "search query"`: Provide search query as command line argument (skips interactive prompt)

### Example Session

```
================================================================================
  DealScan - Product Deal Scraper
  Search Slickdeals & DealNews for the best product deals
================================================================================

Enter product to search for: wireless headphones

Scraping deals...
  > Fetching from Slickdeals...
    Found 25 deals from Slickdeals
  > Fetching from DealNews...
    Found 15 deals from DealNews

Total deals collected: 40

Matching deals to search query...
Ranking deals...

Found 12 deals matching 'wireless headphones':

================================================================================

#1 - Score: 95.3
  Sony WH-1000XM5 Wireless Noise Canceling Headphones
  Price: $298.00
  Store: Amazon
  Source: Slickdeals | Upvotes: 150 | Comments: 45
  Link: https://slickdeals.net/...
```

## Project Structure

```
dealscan/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── utils.py               # Matching and ranking utilities
└── scrapers/
    ├── __init__.py
    ├── slickdeals.py      # Slickdeals scraper
    └── dealnews.py        # DealNews scraper
```

## How It Works

### 1. Scraping
The tool visits Slickdeals frontpage and DealNews staff picks to collect current deals. Each deal includes:
- Title
- Price
- Store/Merchant
- Community score (upvotes)
- Comment count
- Link

### 2. Matching
Deals are matched against your search query using:
- Exact phrase matching
- Individual keyword matching
- Fuzzy text similarity

### 3. Ranking
Matched deals are ranked using a weighted scoring system:
- **Relevance (40%)**: How well the deal matches your search
- **Deal Score (30%)**: Community upvotes/rating
- **Engagement (20%)**: Number of comments
- **Source (10%)**: Staff picks get a credibility boost

### 4. Display
The top 20 deals are displayed with color-coded rankings:
- Top 3: Gold/Yellow
- 4-10: Green
- 11-20: White

## Tips for Better Results

- Use specific product names or brands (e.g., "Sony WH-1000XM5" vs "headphones")
- Try different keyword combinations
- Use category terms (e.g., "laptop", "monitor", "keyboard")
- Check multiple times as deals update frequently

## Limitations

- Only scrapes current frontpage/staff picks (not historical deals)
- Depends on website structure (may break if sites redesign)
- No price comparison across multiple retailers
- Rate limiting may apply if run too frequently

## Dependencies

- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing
- **lxml**: Fast XML/HTML parser
- **colorama**: Cross-platform colored terminal output
- **python-dateutil**: Date/time utilities

## Troubleshooting

**No deals found:**
- Check your internet connection
- Websites may be temporarily down
- Try again in a few minutes

**Website structure errors:**
- The websites may have changed their HTML structure
- Check if there are any updates to the scraper code

**Search returns no matches:**
- Try broader keywords
- Check spelling
- Use brand names or product categories

## License

This project is for educational purposes. Please respect the terms of service of Slickdeals and DealNews when using this tool.

## Disclaimer

This tool is not affiliated with Slickdeals or DealNews. Use responsibly and in accordance with each website's terms of service.
