import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

# 🔹 Change this to test different domains
test_domain = "x.com"

# 🔹 CSV path
csv_path = "sources_db.csv"

# 🔹 Check if domain already exists
def domain_in_csv(domain):
    if not os.path.exists(csv_path):
        return False
    df = pd.read_csv(csv_path)
    return domain in df["domain"].values

# 🔹 Append to CSV
def append_to_csv(data):
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=["domain", "bias", "credibility_rating", "score", "source", "reason"])
    else:
        df = pd.read_csv(csv_path)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    print(f"✅ Added {data['domain']} to sources_db.csv")

prompt2 = """the last output you gave was for factcheck.org. however when I check manually, its Factual reporting was reported as VERY HIGH. 
Yet you reported a score of 80. Why is this? Please fix this error for any future requests. 
Also if you have a doubt, the "credibility_rating" score is determined by the "Factual Reporting" secion in the MBFC website. Derive this data from there. Do you understand?"""

# 🔹 Gemini call (unchanged)
def fetch_from_gemini(domain):
    prompt3 = f"""for the website "{domain}" please search this domain in the MBFC website and provide me the details in the format as I have shown below:
  {{
    "domain": "nytimes.com",
    "bias": "Left-Center",
    "credibility_rating": "High",
    "score": 88,
    "source": "MBFC",
    "reason": "The New York Times is a well-known news organization with thorough editorial standards and factual reporting. MBFC rates it Left-Center due to editorial stance."
  }}
  dont add json or any other text before and after the curly brackets please"""
    
    response = client.models.generate_content(
        model='gemini-2.0-flash', contents=prompt3
    )
    return json.loads(response.text)

# 🔹 Main logic
if domain_in_csv(test_domain):
    print(f"✅ '{test_domain}' already exists in sources_db.csv")
    df = pd.read_csv(csv_path)
    existing = df[df["domain"] == test_domain].to_dict(orient="records")[0]
    print(json.dumps(existing, indent=2))
else:
    print(f"🌐 '{test_domain}' not found locally. Using Gemini...")
    result = fetch_from_gemini(test_domain)
    print(json.dumps(result, indent=2))
    append_to_csv(result)
