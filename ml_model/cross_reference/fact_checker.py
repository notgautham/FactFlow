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

🗓️ Publication Date: It is given in the starting of the content

Instructions:
1. Assume the article's publication date is your current point in time. Treat this as your **factual world**.
2. All evaluations must use that date as the present. Do not rely on your model's internal date. Assume the article is set in a real and valid timeline unless something contradicts known facts as of that date.
3. ⚠️ Do NOT reject or dispute claims simply because you are unaware of recent developments. Only flag claims that are provably false or logically inconsistent **based on verified knowledge up to and including the publication date**.
4. If you cannot verify or refute a claim, or if it is plausible but unconfirmed, **skip it**.
5. Do not use speculative language like “requires confirmation” or “seems unusual.” This layer only flags **clear factual errors**.
6. Include only the clearly false or impossible claims in the `issues` list.
7. If the article appears fully accurate, return a `verdict` of `"factual"`.


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
