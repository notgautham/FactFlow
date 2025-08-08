from ml_model.trained_models.pattern_verification import analyze_content
from ml_model.source_credibility.fallback_lookup import get_source_credibility
from ml_model.cross_reference.fact_checker import check_article_factuality
from urllib.parse import urlparse

def run_all_verifications(title: str, content: str, url: str) -> dict:
    full_text = title.strip() + "\n" + content.strip()
    result = {"details": {}}
    print("\n🚀 Starting FactFlow Analysis Pipeline")

    # Pattern Detection Layer
    print("🔍 Running Pattern Verification...")
    try:
        pattern_result = analyze_content(full_text)
        pattern_label = pattern_result.get("label")
        pattern_confidence = pattern_result.get("confidence", 0)
        pattern_reason = {
            "FAKE": "The content contains clickbait phrases, emotional triggers, or stylistic patterns typically seen in fake news.",
            "SOFT_FAKE": "The article includes some sensational or vague language, which might be misleading even if not outright false.",
            "REAL": "The writing style appears professional and lacks typical fake news patterns like excessive emotion or exaggeration."
        }.get(pattern_label, "Pattern analysis could not determine the tone conclusively.")
        result["details"]["pattern_verification"] = {
            "label": pattern_label,
            "confidence": round(pattern_confidence, 4),
            "probabilities": pattern_result.get("probabilities", {}),
            "reason": pattern_reason
        }
        print("✅ Pattern Verification Complete")
    except Exception as e:
        print("❌ Pattern Verification Failed:", e)
        result["details"]["pattern_verification"] = {"error": str(e)}

    # Source Credibility Layer
    print("🔍 Running Source Credibility...")
    try:
        domain = extract_domain(url)
        source_result = get_source_credibility(domain)

        raw_score = source_result.get("score", 0)
        try:
            score = int(raw_score)
        except (ValueError, TypeError):
            score = 0

        source_note = (
            "This source is generally considered reliable."
            if score >= 70 else
            "Caution: This source may lack high credibility."
        )

        result["details"]["source_credibility"] = {
            "domain": domain,
            "score": score,
            "credibility_rating": source_result.get("credibility_rating", "N/A"),
            "bias": source_result.get("bias", "N/A"),
            "source": source_result.get("source", "MBFC"),
            "reason": source_result.get("reason", "N/A"),
            "note": source_note
        }
        print("✅ Source Credibility Check Complete")
    except Exception as e:
        print("❌ Source Credibility Failed:", e)
        result["details"]["source_credibility"] = {"error": str(e)}

    # Factual Verification Layer
    print("🔍 Running Cross Reference Verification...")
    try:
        factual_result = check_article_factuality(full_text)
        factual_verdict = factual_result.get("verdict", "")
        result["details"]["cross_reference"] = {
            "verdict": factual_verdict,
            "summary": factual_result.get("summary", ""),
            "issues": factual_result.get("issues", []),
            "supporting_sources": factual_result.get("supporting_sources", [])
        }
        print("✅ Cross Reference Complete")
    except Exception as e:
        print("❌ Cross Reference Failed:", e)
        result["details"]["cross_reference"] = {"error": str(e)}

    # Final Verdict
    print("🧠 Computing Final Verdict...")
    final = decide_final_verdict(
        result["details"].get("pattern_verification", {}),
        result["details"].get("source_credibility", {}),
        result["details"].get("cross_reference", {})
    )
    result["verdict"] = final["verdict"]
    result["explanation"] = final["explanation"]
    print("✅ Verdict:", final["verdict"])
    return result


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    return hostname[4:] if hostname.startswith("www.") else hostname


def decide_final_verdict(pattern: dict, source: dict, factual: dict) -> dict:
    pattern_label = (pattern.get("label") or "").upper()
    factual_verdict = (factual.get("verdict") or "").lower()

    source_rating = (source.get("credibility_rating") or "").lower()
    try:
        score = int(source.get("score", 0))
    except (ValueError, TypeError):
        score = 0

    is_source_not_rated = source_rating in ["n/a", "not rated"]

    # STRONG FAKE SIGNALS (Layer 2 or 3)
    if source_rating in ["satire", "questionable"] or 0 < score < 20:
        return {
            "verdict": "Fake",
            "explanation": "The source is classified as satire or extremely low credibility, and cannot be trusted for factual content."
        }

    if factual_verdict == "factually incorrect":
        if score < 50 or is_source_not_rated:
            return {
                "verdict": "Fake",
                "explanation": "The article contains factually incorrect claims and either comes from an untrusted or unknown source."
            }
        else:
            return {
                "verdict": "Soft Fake",
                "explanation": "Despite coming from a moderately credible source, the article has verifiable factual inaccuracies."
            }

    # MIXED / STYLISTIC CONCERNS
    if factual_verdict == "somewhat factual":
        if pattern_label in ["FAKE", "SOFT_FAKE"]:
            return {
                "verdict": "Soft Fake",
                "explanation": "The article contains speculative or stylistically misleading content, with some factual inconsistencies."
            }
        elif pattern_label == "REAL":
            if score >= 70:
                return {
                    "verdict": "Uncertain",
                    "explanation": "The article is from a trusted source and is well-written, but has some factual inconsistencies."
                }
            elif is_source_not_rated:
                return {
                    "verdict": "Uncertain",
                    "explanation": "The article is written credibly and partially factual, but the source is not rated."
                }
            else:
                return {
                    "verdict": "Soft Fake",
                    "explanation": "Despite good style, the article has factual gaps and originates from a moderately rated source."
                }

    # ALL GOOD
    if factual_verdict == "factual":
        if pattern_label == "REAL":
            if score >= 70 or source_rating == "high":
                return {
                    "verdict": "Likely Real",
                    "explanation": "The article is factually accurate, written in a credible style, and comes from a highly rated source."
                }
            elif is_source_not_rated:
                return {
                    "verdict": "Likely Real",
                    "explanation": "The article is factually accurate and well-written, although the source is not rated."
                }
            else:
                return {
                    "verdict": "Uncertain",
                    "explanation": "The article seems accurate and well-written, but the source has only moderate credibility."
                }
        elif pattern_label in ["SOFT_FAKE", "FAKE"]:
            return {
                "verdict": "Soft Fake",
                "explanation": "While the article is factually correct, its writing style reflects clickbait or emotional manipulation."
            }

    # Default fallback
    return {
        "verdict": "Uncertain",
        "explanation": "The evidence from the verification layers is mixed or insufficient to make a clear decision."
    }