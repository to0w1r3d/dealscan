# Web Scraping Compliance Guide

## Overview

DealScan is designed to scrape deal information from Slickdeals and DealNews in a **legal, ethical, and compliant** manner. Both sites have been analyzed and found to have **0/10 scraping difficulty**, with clear robots.txt permissions.

## Scraping Permissions

### Slickdeals.net

**robots.txt Analysis:**
- ✅ **Allowed**: All user-agents can scrape
- ✅ **No crawl-delay specified**: Use reasonable delays (1-2 seconds recommended)
- ✅ **Difficulty**: 0/10 (Easy)
- ✅ **TLS Fingerprinting**: None detected
- ✅ **Rate Limiting**: Minimal (no blocking after 12 requests)

**Recommended Practice:**
```python
from scrapers.slickdeals_advanced import SlickdealsAdvancedScraper
import time
import random

scraper = SlickdealsAdvancedScraper()

# Use 1-2 second delays between requests
time.sleep(random.uniform(1, 2))
deals = scraper.scrape_deals()
```

### DealNews.com

**robots.txt Analysis:**
- ✅ **Allowed**: All user-agents can scrape
- ⚠️ **Crawl-delay REQUIRED**: 2.0 seconds (specified in robots.txt)
- ✅ **Difficulty**: 0/10 (Easy)
- ✅ **TLS Fingerprinting**: None detected
- ✅ **Rate Limiting**: Minimal (no blocking after 12 requests)

**Compliance Requirement:**
```python
from scrapers.dealnews_advanced import DealNewsAdvancedScraper

# DealNews scraper automatically enforces 2.0 second crawl-delay
scraper = DealNewsAdvancedScraper()
deals = scraper.scrape_deals()  # Automatic compliance
```

## Legal Compliance

### robots.txt Protocol (RFC 9309)

DealScan **fully complies** with the robots.txt standard:

1. **Respects robots.txt directives**
   - Follows allowed/disallowed paths
   - Honors crawl-delay specifications
   - Uses appropriate User-Agent strings

2. **Crawl-Delay Enforcement**
   - DealNews: Automatically enforces 2.0s delay
   - Slickdeals: Uses 1-2s delays as best practice

3. **Rate Limiting**
   - Never exceeds 1 request per second
   - Implements exponential backoff on errors
   - Respects server response codes (429, 503)

### Terms of Service Considerations

**Important**: Before deploying to production:

1. **Review Terms of Service**
   - Read Slickdeals ToS: https://slickdeals.net/terms.html
   - Read DealNews ToS: https://www.dealnews.com/about/terms-conditions/

2. **Common ToS Restrictions**
   - ❌ Don't resell scraped data
   - ❌ Don't use data to compete directly
   - ✅ Can use for personal research/aggregation
   - ✅ Can build derivative tools (usually)

3. **Attribution**
   - Provide clear attribution to source
   - Link back to original deals
   - Don't misrepresent data source

### Best Practices

1. **Identify Your Bot**
```python
headers = {
    'User-Agent': 'DealScanBot/1.0 (+https://github.com/yourusername/dealscan)'
}
```

2. **Handle Errors Gracefully**
```python
if response.status_code == 429:  # Too Many Requests
    time.sleep(60)  # Back off for 1 minute
elif response.status_code == 503:  # Service Unavailable
    time.sleep(300)  # Back off for 5 minutes
```

3. **Respect Bandwidth**
```python
# Don't scrape more often than necessary
MINIMUM_SCRAPE_INTERVAL = 300  # 5 minutes
```

## Ethical Scraping Guidelines

### DO:
✅ Respect crawl-delay directives (especially DealNews 2.0s)
✅ Use reasonable request rates (1-2 seconds between requests)
✅ Cache results to avoid repeat requests
✅ Identify your bot with User-Agent
✅ Handle errors and retry with exponential backoff
✅ Monitor server responses (respect 429, 503 codes)
✅ Provide attribution to data sources
✅ Follow robots.txt directives

### DON'T:
❌ Scrape faster than crawl-delay allows
❌ Make concurrent requests to same domain
❌ Ignore error responses (429, 503)
❌ Scrape during peak hours unnecessarily
❌ Extract PII (personally identifiable information)
❌ Circumvent security measures
❌ Misrepresent data source
❌ Violate terms of service

## Implementation Checklist

### Development Phase
- [x] Implement robots.txt compliance
- [x] Add crawl-delay enforcement (2.0s for DealNews)
- [x] Use proper User-Agent strings
- [x] Implement error handling
- [x] Add request rate limiting
- [x] Create demo mode for testing

### Pre-Production
- [ ] Review both sites' Terms of Service
- [ ] Obtain residential IP or proxy
- [ ] Set up monitoring and logging
- [ ] Implement caching to reduce requests
- [ ] Test rate limiting in production environment
- [ ] Create documentation for users

### Production
- [ ] Monitor scraping success rates
- [ ] Watch for 429/503 responses
- [ ] Respect any IP blocks (don't circumvent)
- [ ] Keep User-Agent updated
- [ ] Maintain crawl-delay compliance
- [ ] Regular ToS compliance reviews

## Monitoring Compliance

### Logging Requests

```python
import logging

logging.basicConfig(
    filename='scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log every request
logger.info(f"Requesting {url}")
logger.info(f"Response: {response.status_code} in {elapsed}s")
logger.info(f"Crawl-delay compliance: {elapsed >= required_delay}")
```

### Metrics to Track

1. **Request Rate**
   - Requests per minute
   - Average delay between requests
   - Crawl-delay compliance rate

2. **Response Codes**
   - 200: Success
   - 403: Forbidden (IP blocked)
   - 429: Too Many Requests (slow down)
   - 503: Service Unavailable (back off)

3. **Success Rate**
   - Percentage of successful scrapes
   - Number of deals extracted
   - Parse errors

### Automated Compliance Checks

```python
class ComplianceMonitor:
    def __init__(self):
        self.request_times = []
        self.required_delay = 2.0  # DealNews requirement

    def check_delay_compliance(self):
        if len(self.request_times) < 2:
            return True

        last_two = self.request_times[-2:]
        actual_delay = last_two[1] - last_two[0]

        if actual_delay < self.required_delay:
            logger.warning(
                f"Crawl-delay violation: {actual_delay:.2f}s "
                f"(required: {self.required_delay}s)"
            )
            return False

        return True

    def log_request(self):
        self.request_times.append(time.time())
        return self.check_delay_compliance()
```

## When to Stop Scraping

Stop scraping immediately if:

1. **429 (Too Many Requests)**
   - Wait at least 1 hour before retrying
   - Review and increase delays

2. **403 (Forbidden)**
   - Your IP may be blocked
   - Don't attempt to circumvent
   - Contact site owner if needed

3. **Legal Notice**
   - If you receive cease & desist
   - Stop immediately and consult legal counsel

4. **Terms of Service Update**
   - Review new terms
   - Adjust scraping accordingly
   - May need to stop if prohibited

## Contact Information

If you receive a block or notice:

1. **Don't panic** - it may be temporary
2. **Review logs** - check compliance
3. **Contact site owner** - be transparent
4. **Consider alternatives** - official APIs, partnerships

## Alternative Approaches

If scraping becomes problematic:

1. **Official APIs**
   - Check for affiliate programs
   - Request API access
   - Partner with the platform

2. **RSS Feeds**
   - Many sites offer RSS
   - Less likely to be blocked
   - Limited but reliable

3. **Data Partnerships**
   - Contact business development
   - Formal data sharing agreement
   - Legitimate and sustainable

## Summary

**DealScan is designed to be compliant:**

- ✅ Respects robots.txt (including 2.0s crawl-delay for DealNews)
- ✅ Uses reasonable request rates
- ✅ Identifies itself properly
- ✅ Handles errors gracefully
- ✅ Provides proper attribution
- ✅ Follows ethical scraping guidelines

**Your responsibility:**
- Review Terms of Service before production use
- Monitor compliance continuously
- Respect any blocks or notices
- Use responsibly and ethically

## References

- **robots.txt RFC**: https://www.rfc-editor.org/rfc/rfc9309.html
- **Ethical Web Scraping**: https://www.scrapehero.com/web-scraping-laws-and-ethics/
- **Slickdeals ToS**: https://slickdeals.net/terms.html
- **DealNews ToS**: https://www.dealnews.com/about/terms-conditions/

---

**Last Updated**: 2025-10-22
**Version**: 1.0
**Review Frequency**: Quarterly or upon ToS changes
