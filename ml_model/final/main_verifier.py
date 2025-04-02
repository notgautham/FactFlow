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

        # 🔒 Safe score conversion
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

    # Final Verdict Decision
    print("🧠 Computing Final Verdict...")
    final_verdict, explanation = decide_final_verdict(
        result["details"].get("pattern_verification", {}),
        result["details"].get("source_credibility", {}),
        result["details"].get("cross_reference", {})
    )
    result["verdict"] = final_verdict
    result["explanation"] = explanation
    print("✅ Verdict:", final_verdict)

    return result


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    return hostname[4:] if hostname.startswith("www.") else hostname


def decide_final_verdict(pattern: dict, source: dict, factual: dict) -> tuple:
    pattern_label = pattern.get("label")
    factual_verdict = factual.get("verdict")

    # 🔒 Safe score conversion again (defensive programming)
    raw_score = source.get("score", 0)
    try:
        score = int(raw_score)
    except (ValueError, TypeError):
        score = 0

    if pattern_label == "FAKE" and factual_verdict == "factually incorrect":
        return "Strong Fake", "The article contains fabricated claims and exhibits deceptive language patterns."

    if pattern_label in ["FAKE", "SOFT_FAKE"] or factual_verdict == "somewhat factual":
        return "Soft Fake", "The article contains speculative or partially unverified claims, or shows stylistic signs of sensationalism."

    if score < 50:
        return "Uncertain", "The source domain has low or unknown credibility, reducing confidence in the content's reliability."

    if factual_verdict == "factual" and pattern_label == "REAL" and source.get("credibility_rating") == "High":
        return "Likely Real", "This article is well-written, factually supported, and published by a highly credible source."

    return "Uncertain", "The evidence from all verification layers is inconclusive."
