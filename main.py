#!/usr/bin/env python3
"""
DealScan - Product Deal Scraper
Searches Slickdeals and DealNews for product deals and ranks them.
"""
import sys
import argparse
from typing import List, Dict
from colorama import init, Fore, Style
from scrapers.slickdeals import SlickdealsScraper
from scrapers.dealnews import DealNewsScraper
from utils import DealMatcher, DealRanker, format_price, truncate_title

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def print_banner():
    """Print application banner."""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}  DealScan - Product Deal Scraper")
    print(f"{Fore.CYAN}  Search Slickdeals & DealNews for the best product deals")
    print(f"{Fore.CYAN}{'='*80}\n")


def get_search_query() -> str:
    """Prompt user for search query."""
    try:
        query = input(f"{Fore.GREEN}Enter product to search for: {Style.RESET_ALL}").strip()
        if not query:
            print(f"{Fore.RED}Error: Search query cannot be empty{Style.RESET_ALL}")
            sys.exit(1)
        return query
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Search cancelled{Style.RESET_ALL}")
        sys.exit(0)


def scrape_all_deals(demo_mode: bool = False) -> List[Dict]:
    """Scrape deals from all sources."""
    if demo_mode:
        print(f"\n{Fore.YELLOW}[DEMO MODE] Using sample deal data...{Style.RESET_ALL}")
        from demo_data import SAMPLE_DEALS
        print(f"{Fore.GREEN}Loaded {len(SAMPLE_DEALS)} sample deals{Style.RESET_ALL}\n")
        return SAMPLE_DEALS

    print(f"\n{Fore.YELLOW}Scraping deals...{Style.RESET_ALL}")

    all_deals = []

    # Scrape Slickdeals
    print(f"  {Fore.CYAN}> Fetching from Slickdeals...{Style.RESET_ALL}")
    slickdeals_scraper = SlickdealsScraper()
    slickdeals_deals = slickdeals_scraper.scrape_deals()
    all_deals.extend(slickdeals_deals)
    if slickdeals_deals:
        print(f"    {Fore.GREEN}Found {len(slickdeals_deals)} deals from Slickdeals{Style.RESET_ALL}")
    else:
        print(f"    {Fore.YELLOW}No deals retrieved from Slickdeals (may be blocked){Style.RESET_ALL}")

    # Scrape DealNews
    print(f"  {Fore.CYAN}> Fetching from DealNews...{Style.RESET_ALL}")
    dealnews_scraper = DealNewsScraper()
    dealnews_deals = dealnews_scraper.scrape_deals()
    all_deals.extend(dealnews_deals)
    if dealnews_deals:
        print(f"    {Fore.GREEN}Found {len(dealnews_deals)} deals from DealNews{Style.RESET_ALL}")
    else:
        print(f"    {Fore.YELLOW}No deals retrieved from DealNews (may be blocked){Style.RESET_ALL}")

    if all_deals:
        print(f"\n{Fore.GREEN}Total deals collected: {len(all_deals)}{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}No deals retrieved. Sites may have anti-bot protection.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Try running with --demo flag to see how the program works:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  python main.py --demo{Style.RESET_ALL}\n")

    return all_deals


def display_results(deals: List[Dict], query: str):
    """Display ranked deals to user."""
    if not deals:
        print(f"{Fore.YELLOW}No deals found matching '{query}'{Style.RESET_ALL}")
        print(f"\nTry:")
        print(f"  - Using different keywords")
        print(f"  - Broader search terms")
        print(f"  - Brand names or product categories")
        return

    print(f"\n{Fore.GREEN}Found {len(deals)} deals matching '{query}':{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    for idx, deal in enumerate(deals[:20], 1):  # Show top 20
        # Determine color based on rank
        if idx <= 3:
            rank_color = Fore.YELLOW
        elif idx <= 10:
            rank_color = Fore.GREEN
        else:
            rank_color = Fore.WHITE

        print(f"\n{rank_color}#{idx} - Score: {deal['final_score']:.1f}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}{Style.BRIGHT}{truncate_title(deal['title'])}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Price: {format_price(deal['price'])}{Style.RESET_ALL}")
        print(f"  Store: {deal['store']}")
        print(f"  Source: {deal['source']} | " +
              f"Upvotes: {deal['score']} | " +
              f"Comments: {deal['comments']}")
        print(f"  {Fore.BLUE}Link: {deal['link']}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    if len(deals) > 20:
        print(f"\n{Fore.YELLOW}Showing top 20 of {len(deals)} matching deals{Style.RESET_ALL}")


def main():
    """Main application entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='DealScan - Search and rank product deals from Slickdeals and DealNews'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run in demo mode with sample data (useful if sites block scraping)'
    )
    parser.add_argument(
        '-q', '--query',
        type=str,
        help='Search query (if not provided, will prompt interactively)'
    )

    args = parser.parse_args()

    print_banner()

    if args.demo:
        print(f"{Fore.CYAN}Running in DEMO mode with sample data{Style.RESET_ALL}\n")

    # Get search query from user or command line
    if args.query:
        query = args.query
        print(f"{Fore.GREEN}Searching for: {query}{Style.RESET_ALL}")
    else:
        query = get_search_query()

    # Scrape deals from all sources
    all_deals = scrape_all_deals(demo_mode=args.demo)

    if not all_deals:
        print(f"{Fore.RED}Failed to retrieve any deals.{Style.RESET_ALL}")
        if not args.demo:
            print(f"{Fore.YELLOW}Try running with --demo flag to see how the program works.{Style.RESET_ALL}")
        sys.exit(1)

    # Match deals to query
    print(f"{Fore.YELLOW}Matching deals to search query...{Style.RESET_ALL}")
    matched_deals = DealMatcher.match_deals(all_deals, query)

    # Rank matched deals
    if matched_deals:
        print(f"{Fore.YELLOW}Ranking deals...{Style.RESET_ALL}")
        ranked_deals = DealRanker.rank_deals(matched_deals)
    else:
        ranked_deals = []

    # Display results
    display_results(ranked_deals, query)

    print(f"\n{Fore.GREEN}Search complete!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
