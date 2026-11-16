"""Web content mining - step 1: collect data.

Scrapes quotes, authors and tags from https://quotes.toscrape.com,
a website that exists specifically for practising web scraping.
"""
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "college-web-mining-project/1.0"}


def parse_page(html):
    """Extract quotes from one page of HTML. Returns (list_of_dicts, has_next_page)."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for block in soup.select("div.quote"):
        rows.append(
            {
                "text": block.select_one("span.text").get_text(strip=True).strip("“”\""),
                "author": block.select_one("small.author").get_text(strip=True),
                "tags": ",".join(t.get_text(strip=True) for t in block.select("a.tag")),
            }
        )
    has_next = soup.select_one("li.next") is not None
    return rows, has_next


def scrape(max_pages=10, delay=1.0):
    """Scrape up to `max_pages` pages and return a pandas DataFrame."""
    all_rows = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/page/{page}/"
        print(f"Scraping {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        rows, has_next = parse_page(response.text)
        all_rows.extend(rows)
        if not has_next:
            break
        time.sleep(delay)  # be polite to the server
    return pd.DataFrame(all_rows)
