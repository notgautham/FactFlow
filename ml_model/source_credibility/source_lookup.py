# source_lookup.py

import pandas as pd
from urllib.parse import urlparse
import os

# Load credibility database
CSV_FILE = os.path.join(os.path.dirname(__file__), "sources_db.csv")
df = pd.read_csv(CSV_FILE)

def extract_domain(url):
    """
    Extracts and normalizes the main domain from a full URL.
    Example: https://www.breitbart.com/news → breitbart.com
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        domain = ".".join(domain_parts[-2:])
    return domain

def check_source_credibility(url):
    """
    Checks the source credibility of a URL by matching its domain against the local CSV database.
    """
    domain = extract_domain(url)
    match = df[df['domain'] == domain]

    if not match.empty:
        row = match.iloc[0]
        return {
            "input_url": url,
            "domain": domain,
            "credibility_rating": row["credibility_rating"],
            "bias": row["bias"],
            "score": int(row["score"]),
            "source": row["source"],
            "reason": row["reason"]
        }
    else:
        return {
            "input_url": url,
            "domain": domain,
            "credibility_rating": "Unknown",
            "bias": "Unknown",
            "score": 50,
            "source": "Local DB",
            "reason": "Domain not found in local credibility database."
        }

# If run directly, perform a test
if __name__ == "__main__":
    test_url = "https://www.breitbart.com/politics/2024/03/25/some-article-title/"
    result = check_source_credibility(test_url)
    import json
    print(json.dumps(result, indent=4))
