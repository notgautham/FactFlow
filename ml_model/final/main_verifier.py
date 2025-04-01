# /ml_model/final/main_verifier.py

from ml_model.trained_models.pattern_verification import analyze_content
from ml_model.source_credibility.fallback_lookup import get_source_credibility
from ml_model.cross_reference.fact_checker import check_article_factuality


def run_all_verifications(title: str, content: str, url: str) -> dict:
    full_text = title.strip() + "\n" + content.strip()

    # Run pattern-based analysis
    pattern_result = analyze_content(full_text)

    # Extract domain from URL
    domain = extract_domain(url)
    source_result = get_source_credibility(domain)

    # Run factual cross-reference
    factual_result = check_article_factuality(full_text)

    # Final verdict
    final_verdict = decide_final_verdict(pattern_result, source_result, factual_result)

    return {
        "pattern_verification": pattern_result,
        "source_credibility": source_result,
        "cross_reference": factual_result,
        "verdict": final_verdict
    }


def extract_domain(url: str) -> str:
    """Extracts domain from full URL (e.g., https://www.cnn.com/article → cnn.com)"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


def decide_final_verdict(pattern: dict, source: dict, factual: dict) -> str:
    """Basic rule-based engine to combine 3 results into one verdict"""
    if pattern.get("label") == "FAKE" and factual.get("verdict") == "factually incorrect":
        return "Strong Fake"
    if factual.get("verdict") == "somewhat factual" or source.get("credibility_rating") == "Mixed":
        return "Soft Fake"
    if factual.get("verdict") == "factual" and pattern.get("label") == "REAL" and source.get("credibility_rating") == "High":
        return "Likely Real"
    return "Uncertain"
