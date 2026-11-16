"""Web content mining - step 2: clean, analyse and visualise the scraped data."""
import re
from collections import Counter

import matplotlib

matplotlib.use("Agg")  # save charts to files, no window needed
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer


def clean_text(text):
    """Lowercase and keep letters only."""
    return re.sub(r"[^a-z\s]", "", str(text).lower())


def word_frequency(df, top_n=15):
    """Most common words (stop words removed) across all quotes."""
    words = []
    for text in df["text"]:
        words += [w for w in clean_text(text).split() if w not in ENGLISH_STOP_WORDS and len(w) > 2]
    return Counter(words).most_common(top_n)


def top_tags(df, top_n=10):
    tags = [t for row in df["tags"].fillna("") for t in row.split(",") if t]
    return Counter(tags).most_common(top_n)


def top_authors(df, top_n=10):
    return df["author"].value_counts().head(top_n)


def cluster_quotes(df, n_clusters=4):
    """Group similar quotes using TF-IDF + K-Means. Returns df with a 'cluster' column
    and a dict of the top keywords for each cluster."""
    n_clusters = min(n_clusters, len(df))
    cleaned = df["text"].apply(clean_text)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
    matrix = vectorizer.fit_transform(cleaned)
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit(matrix)

    df = df.copy()
    df["cluster"] = model.labels_
    terms = vectorizer.get_feature_names_out()
    keywords = {}
    for c in range(n_clusters):
        top_idx = model.cluster_centers_[c].argsort()[::-1][:5]
        keywords[c] = [terms[i] for i in top_idx]
    return df, keywords


def _bar_chart(labels, values, title, xlabel, path):
    plt.figure(figsize=(8, 5))
    plt.barh(labels[::-1], values[::-1], color="#3b7dd8")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()


def run_analysis(df, out_dir="outputs"):
    """Run every analysis, save charts + a text report, and return the report text."""
    lines = [f"Total quotes analysed: {len(df)}", f"Unique authors: {df['author'].nunique()}", ""]

    words = word_frequency(df)
    _bar_chart([w for w, _ in words], [c for _, c in words], "Top words in quotes", "Count", f"{out_dir}/top_words.png")
    lines.append("Top words: " + ", ".join(f"{w}({c})" for w, c in words))

    tags = top_tags(df)
    _bar_chart([t for t, _ in tags], [c for _, c in tags], "Most common tags", "Count", f"{out_dir}/top_tags.png")
    lines.append("Top tags: " + ", ".join(f"{t}({c})" for t, c in tags))

    authors = top_authors(df)
    _bar_chart(list(authors.index), list(authors.values), "Authors with most quotes", "Quotes", f"{out_dir}/top_authors.png")
    lines.append("Top authors: " + ", ".join(f"{a}({c})" for a, c in authors.items()))

    clustered, keywords = cluster_quotes(df)
    clustered.to_csv(f"{out_dir}/quotes_with_clusters.csv", index=False)
    lines.append("\nQuote clusters (K-Means on TF-IDF):")
    for c, kw in keywords.items():
        size = int((clustered["cluster"] == c).sum())
        lines.append(f"  Cluster {c} ({size} quotes): {', '.join(kw)}")

    report = "\n".join(lines)
    with open(f"{out_dir}/report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    return report
