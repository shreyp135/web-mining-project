import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd

from src.analyze import cluster_quotes, top_tags, word_frequency
from src.scraper import parse_page

HTML = """
<div class="quote">
  <span class="text">“Life is what you make it.”</span>
  <span>by <small class="author">Test Author</small></span>
  <div class="tags"><a class="tag">life</a><a class="tag">motivation</a></div>
</div>
<nav><ul class="pager"><li class="next"><a href="/page/2/">Next</a></li></ul></nav>
"""


def test_parse_page():
    rows, has_next = parse_page(HTML)
    assert len(rows) == 1
    assert rows[0]["author"] == "Test Author"
    assert rows[0]["text"] == "Life is what you make it."
    assert rows[0]["tags"] == "life,motivation"
    assert has_next is True


def test_analysis_on_sample():
    df = pd.read_csv("data/sample_quotes.csv")
    assert word_frequency(df)
    assert top_tags(df)
    clustered, keywords = cluster_quotes(df, n_clusters=3)
    assert "cluster" in clustered.columns and len(keywords) == 3
