import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_CREDIBILITY")
if not api_key:
    raise Exception("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)
csv_path = "sources_db.csv"

# Build prompt for Gemini
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

# Gemini API fallback
def fetch_from_gemini(domain):
    prompt = build_prompt(domain)
    response = client.models.generate_content(
        model='gemini-2.0-flash', contents=prompt
    )
    return json.loads(response.text)

# Check local CSV
def domain_in_csv(domain):
    if not os.path.exists(csv_path):
        return False
    df = pd.read_csv(csv_path)
    return domain in df["domain"].values

# Append new row
def append_to_csv(data):
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=["domain", "bias", "credibility_rating", "score", "source", "reason"])
    else:
        df = pd.read_csv(csv_path)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    print(f"✅ Added {data['domain']} to sources_db.csv")

# ✅ This is the function to import and use in your backend
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

# Optional CLI test
if __name__ == "__main__":
    test_domain = "factcheck.org"  # Change for testing
    output = get_source_credibility(test_domain)
    print(json.dumps(output, indent=2))
