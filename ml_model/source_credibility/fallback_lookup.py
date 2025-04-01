# /ml_model/source_credibility/fallback_lookup.py

import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_CREDIBILITY")
if not api_key:
    raise Exception("❌ GEMINI_API_KEY_CREDIBILITY not found in .env file")

client = genai.Client(api_key=api_key)

# Absolute path to sources_db.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "sources_db.csv")

def build_prompt(domain):
    return f"""
for the website "{domain}" please search this domain in the MBFC website and provide me the details in the format as I have shown below:
{{
  "domain": "nytimes.com",
  "bias": "Left-Center",
  "credibility_rating": "High",
  "score": 88,
  "source": "MBFC",
  "reason": "The New York Times is a well-known news organization with thorough editorial standards and factual reporting. MBFC rates it Left-Center due to editorial stance."
}}
dont add json or any other text before and after the curly brackets please
"""

def fetch_from_gemini(domain):
    prompt = build_prompt(domain)
    response = client.models.generate_content(
        model='gemini-2.0-flash', contents=prompt
    )
    raw_text = response.text.strip()

    # Remove optional Markdown-style code block
    if raw_text.startswith("```json") and raw_text.endswith("```"):
        raw_text = raw_text[7:-3].strip()
    elif raw_text.startswith("```") and raw_text.endswith("```"):
        raw_text = raw_text[3:-3].strip()

    try:
        return json.loads(raw_text)
    except Exception as e:
        raise Exception("❌ Failed to parse Gemini response:\n" + str(e) + "\nRaw text:\n" + response.text)


def domain_in_csv(domain):
    if not os.path.exists(csv_path):
        return False
    df = pd.read_csv(csv_path)
    return domain in df["domain"].values

def append_to_csv(data):
    # Skip saving if credibility rating is N/A (i.e., not found in MBFC)
    if data.get("credibility_rating", "N/A") == "N/A":
        print(f"⚠️ Not adding '{data['domain']}' to CSV because it was not found in MBFC.")
        return

    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=["domain", "bias", "credibility_rating", "score", "source", "reason"])
    else:
        df = pd.read_csv(csv_path)

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    print(f"✅ Added {data['domain']} to sources_db.csv")


def get_source_credibility(domain):
    if domain_in_csv(domain):
        df = pd.read_csv(csv_path)
        record = df[df["domain"] == domain].to_dict(orient="records")[0]
        return record
    else:
        print(f"🌐 Domain '{domain}' not found in CSV. Querying Gemini...")
        result = fetch_from_gemini(domain)
        if result:
            append_to_csv(result)
        return result
