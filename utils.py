"""Utility functions for deal matching and ranking."""
import re
from typing import List, Dict
from difflib import SequenceMatcher


class DealMatcher:
    """Match and rank deals based on search query."""

    @staticmethod
    def match_deals(deals: List[Dict], query: str) -> List[Dict]:
        """
        Filter deals that match the search query.

        Args:
            deals: List of deal dictionaries
            query: Search query string

        Returns:
            List of matching deals with relevance scores
        """
        query_lower = query.lower()
        query_terms = query_lower.split()

        matched_deals = []

        for deal in deals:
            relevance = DealMatcher._calculate_relevance(deal, query_lower, query_terms)

            if relevance > 0:
                deal['relevance_score'] = relevance
                matched_deals.append(deal)

        return matched_deals

    @staticmethod
    def _calculate_relevance(deal: Dict, query_lower: str, query_terms: List[str]) -> float:
        """
        Calculate relevance score for a deal based on query.

        Scoring:
        - Exact query match in title: 100 points
        - Partial query match: 50 points
        - All query terms present: 40 points
        - Some query terms present: 10 points per term
        - Similarity ratio bonus: up to 30 points
        """
        title_lower = deal.get('title', '').lower()
        score = 0

        # Exact match
        if query_lower in title_lower:
            score += 100

        # Check for all query terms
        terms_found = sum(1 for term in query_terms if term in title_lower)

        if terms_found == len(query_terms) and len(query_terms) > 1:
            score += 40
        else:
            score += terms_found * 10

        # Similarity ratio
        similarity = SequenceMatcher(None, query_lower, title_lower).ratio()
        score += similarity * 30

        return score


class DealRanker:
    """Rank deals by combined score of relevance and deal quality."""

    @staticmethod
    def rank_deals(deals: List[Dict]) -> List[Dict]:
        """
        Rank deals by combined score.

        Scoring factors:
        - Relevance score (from matching): 40%
        - Deal score/upvotes: 30%
        - Comment count: 20%
        - Source bonus: 10%
        """
        for deal in deals:
            final_score = DealRanker._calculate_final_score(deal)
            deal['final_score'] = final_score

        # Sort by final score (descending)
        ranked_deals = sorted(deals, key=lambda x: x['final_score'], reverse=True)

        return ranked_deals

    @staticmethod
    def _calculate_final_score(deal: Dict) -> float:
        """Calculate final ranking score for a deal."""
        relevance = deal.get('relevance_score', 0)
        deal_score = deal.get('score', 0)
        comments = deal.get('comments', 0)
        source = deal.get('source', '')

        # Normalize scores
        relevance_points = relevance * 0.4
        score_points = min(deal_score, 100) * 0.3  # Cap at 100
        comment_points = min(comments / 5, 20) * 0.2  # Cap at 100 comments
        source_points = 10 if source == 'DealNews' else 8  # Staff picks get slight boost

        final = relevance_points + score_points + comment_points + source_points

        return round(final, 2)


def format_price(price_str: str) -> str:
    """Format price string for display."""
    if not price_str or price_str == "N/A":
        return "Price not listed"
    return price_str


def truncate_title(title: str, max_length: int = 80) -> str:
    """Truncate title to max length."""
    if len(title) <= max_length:
        return title
    return title[:max_length - 3] + "..."
