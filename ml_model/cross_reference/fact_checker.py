# /ml_model/cross_reference/fact_checker.py

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_FACTCHECK")

if not api_key:
    raise Exception("❌ GEMINI_API_KEY_FACTCHECK not found in .env file")

client = genai.Client(api_key=api_key)

def check_article_factuality(article_text):
    prompt_template = f"""
You are a fact-checking expert. Carefully read the following news article and determine its factual accuracy.

🗓️ Publication Date: The article was published on the date given in the starting of the article content. Treat this as the current time and your reference frame for evaluating all claims.

Instructions:
1. Assume the article’s timeline is valid. If it states that Donald Trump is President, accept that as true for the purposes of fact-checking.
2. Do NOT compare your own internal knowledge of events or timelines with the article's stated facts. Focus only on contradictions or impossibilities **within the article itself** or based on well-established facts known up to that date.
3. If a claim is unfamiliar, speculative, or forward-looking (e.g., “will happen tomorrow”), that is not a factual error. Only flag a claim if it is clearly, provably false.
4. Tolerate common journalistic phrasing, such as:
   - “Expected to...” / “Set to announce...” / “May lead to...”
   - Same-day predictions or embargoed events
   - Partial market data reported intraday or post-close
   - Quotes from public officials or spokespersons
5. Do NOT flag stylistic or speculative statements as factual errors.
6. Skip any claims that cannot be confidently confirmed or refuted using information valid on or before the article’s publication date.

📊 VERDICT RULES:
- Use `"factual"` if there are no factual errors or only minor harmless phrasing inconsistencies.
- Use `"somewhat factual"` if there are 1–2 small factual inaccuracies that don't change the overall message.
- Use `"factually incorrect"` ONLY if there are multiple serious factual errors that mislead the reader or contradict reality.

⚠️ Output Format (strict JSON):
{{
  "verdict": "factual" | "somewhat factual" | "factually incorrect",
  "issues": [ {{ "claim": "...", "explanation": "..." }} ],
  "supporting_sources": [ {{ "domain": "...", "url": "..." }} ],
  "summary": "..."
}}

Here is the article content:

{article_text}
""".strip()

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt_template
    )

    raw_text = response.text.strip()

    # Strip Markdown-style backticks if present
    if raw_text.startswith("```json") and raw_text.endswith("```"):
        raw_text = raw_text[7:-3].strip()
    elif raw_text.startswith("```") and raw_text.endswith("```"):
        raw_text = raw_text[3:-3].strip()

    try:
        output = json.loads(raw_text)
        return output
    except Exception as e:
        raise Exception("Failed to parse JSON response: " + str(e) + "\nResponse text: " + response.text)
