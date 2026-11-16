# Web Content Mining: Quotes Scraper & Analyzer

A basic-level **web mining** project written in Python. It collects data from a website (web scraping), cleans the text, and then mines it for patterns using frequency analysis and machine-learning clustering.

## Objective
To demonstrate the core web content mining workflow: **collect → preprocess → analyse → visualise**.

## Data source
[quotes.toscrape.com](https://quotes.toscrape.com), a public sandbox site built for practising web scraping. Collected fields: quote text, author, tags.

## Techniques used
| Step | Technique | Library |
|------|-----------|---------|
| Data collection | HTTP requests + HTML parsing (web scraping) | `requests`, `BeautifulSoup` |
| Preprocessing | Lowercasing, punctuation removal, stop-word removal | `re`, `scikit-learn` |
| Analysis | Word frequency, tag frequency, author counts | `collections.Counter`, `pandas` |
| Mining | TF-IDF vectorisation + K-Means clustering of quotes | `scikit-learn` |
| Visualisation | Bar charts | `matplotlib` |

## Project structure
```
web-mining-project/
├── main.py               # runs the full pipeline
├── requirements.txt
├── src/
│   ├── scraper.py        # scraping + HTML parsing
│   └── analyze.py        # cleaning, mining, charts
├── data/
│   └── sample_quotes.csv # sample data for offline use
├── outputs/              # charts + report.txt (generated)
└── tests/
    └── test_parser.py
```

## How to run
```bash
pip install -r requirements.txt

python main.py                # scrape the live site (up to 10 pages) and analyse
python main.py --pages 3      # scrape only 3 pages
python main.py --offline      # no internet: analyse the bundled sample data

python -m pytest              # run tests
```

## Output
Generated in `outputs/`:
- `top_words.png`, `top_tags.png`, `top_authors.png`: bar charts
- `quotes_with_clusters.csv`: each quote with its cluster number
- `report.txt`: summary of findings and cluster keywords

## How it works
1. **Scrape**: `scraper.py` downloads each page and uses CSS selectors to extract quote, author and tags. It waits 1 second between requests to be polite to the server.
2. **Clean**: text is lowercased and stripped of punctuation; common English stop words are removed.
3. **Analyse**: counts the most frequent words, tags and authors.
4. **Cluster**: quotes are converted to TF-IDF vectors and grouped by K-Means; the top keywords of each cluster describe its theme.

## Limitations & future work
- Only scrapes one site with a fixed HTML layout.
- Could add sentiment analysis, word clouds, or a Flask/Streamlit dashboard.
- Could add web *structure* mining (link analysis) or web *usage* mining (log analysis).

## Ethics
Only a site that explicitly allows scraping practice is used, with a request delay. Always check `robots.txt` and terms of service before scraping other sites.
