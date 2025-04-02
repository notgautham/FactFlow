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

        # Safely convert score to int
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

    # Final Verdict Decision with Advanced Logic
    print("🧠 Computing Final Verdict...")
    final = decide_final_verdict(
        result["details"].get("pattern_verification", {}),
        result["details"].get("source_credibility", {}),
        result["details"].get("cross_reference", {})
    )
    final_verdict = final["verdict"]
    explanation = final["explanation"]
    result["verdict"] = final_verdict
    result["explanation"] = explanation
    print("✅ Verdict:", final_verdict)

    return result


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    return hostname[4:] if hostname.startswith("www.") else hostname


def decide_final_verdict(pattern: dict, source: dict, factual: dict) -> dict:
    # Extract and normalize values
    pattern_label = (pattern.get("label") or "").upper()  # e.g. "FAKE", "SOFT_FAKE", "REAL"
    factual_verdict = (factual.get("verdict") or "").lower()  # e.g. "factually incorrect", "somewhat factual", "factual"
    
    raw_score = source.get("score", 0)
    try:
        score = int(raw_score)
    except (ValueError, TypeError):
        score = 0
    source_rating = (source.get("credibility_rating") or "").lower()  # e.g. "high", "satire", "mixed"

    # Advanced decision tree:
    # CASE 1: If the source is a known satire or has extremely low score, it's Fake.
    if source_rating in ["satire", "questionable"] or score < 20:
        return {
            "verdict": "Fake",
            "explanation": "The source is identified as satirical or extremely low-credibility, and the content is not meant to be taken as factual."
        }

    # CASE 2: If cross-reference shows factually incorrect, final verdict must be Fake.
    if factual_verdict == "factually incorrect":
        return {
            "verdict": "Fake",
            "explanation": "The article contains multiple factually incorrect claims."
        }

    # CASE 3: If pattern is suspicious (FAKE or SOFT_FAKE) or cross-reference is somewhat factual, mark as Soft Fake.
    if pattern_label in ["FAKE", "SOFT_FAKE"] or factual_verdict == "somewhat factual":
        return {
            "verdict": "Soft Fake",
            "explanation": "The article shows speculative or partially unverified claims or stylistic signs of sensationalism."
        }

    # CASE 4: If pattern is REAL, cross-reference is factual, and source is highly credible, mark as Likely Real.
    if pattern_label == "REAL" and factual_verdict == "factual" and (score >= 70 or source_rating == "high"):
        return {
            "verdict": "Likely Real",
            "explanation": "All signals indicate that the article is factual and comes from a highly credible source."
        }

    # Default fallback if signals are mixed.
    return {
        "verdict": "Uncertain",
        "explanation": "The evidence from the verification layers is mixed or inconclusive."
    }
