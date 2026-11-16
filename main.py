"""Run the whole web mining pipeline.

Usage:
    python main.py                 # scrape live website (10 pages) then analyse
    python main.py --pages 3       # scrape fewer pages
    python main.py --offline       # skip scraping, use data/sample_quotes.csv
"""
import argparse
import os

import pandas as pd

from src.analyze import run_analysis
from src.scraper import scrape

RAW_PATH = "data/quotes.csv"
SAMPLE_PATH = "data/sample_quotes.csv"


def main():
    parser = argparse.ArgumentParser(description="Web content mining project")
    parser.add_argument("--pages", type=int, default=10, help="max pages to scrape")
    parser.add_argument("--offline", action="store_true", help="use bundled sample data")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    if args.offline:
        df = pd.read_csv(SAMPLE_PATH)
        print(f"Loaded {len(df)} rows from {SAMPLE_PATH}")
    else:
        df = scrape(max_pages=args.pages)
        df.to_csv(RAW_PATH, index=False)
        print(f"Scraped {len(df)} quotes -> {RAW_PATH}")

    print("\n" + run_analysis(df))
    print("\nCharts and report saved in the outputs/ folder.")


if __name__ == "__main__":
    main()
