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

Instructions:
1. Identify the main claims or statements made in the article.
2. Cross-check these claims against publicly available, trusted knowledge.
3. Flag any factual errors or inconsistencies with clear explanations.
4. If the article appears accurate, state that clearly.
5. If you know that the same topic or claim has been reported by reputable news sources, list them under `supporting_sources`.

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
