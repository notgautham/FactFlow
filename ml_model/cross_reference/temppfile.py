import os
from dotenv import load_dotenv
from google import genai

# ✅ Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("❌ GEMINI_API_KEY not found in .env file")

# ✅ Initialize Gemini client
client = genai.Client(api_key=api_key)

# ✅ Prompt
prompt = "why are you not able to scrape data to verify? Because I want you to be able to verify if a website that I am browsing is making any fake claims. Will you be able to at least search for other articles and cross verify? Is there any other alternative?"

# ✅ Gemini call
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

# ✅ Print response
print(response.text)
