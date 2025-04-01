import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_FACTCHECK")

if not api_key:
    raise Exception("❌ GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

def check_article_factuality(article_text):
    """
    Accepts the contents of a web-scraped news article and returns
    a structured dictionary with the factual reasoning verdict, issues,
    supporting sources, and a summary.
    
    Expected output format:
    {
      "verdict": "factual",
      "issues": [
        {
          "claim": "India has 100 states",
          "explanation": "India has only 28 states."
        }
      ],
      "supporting_sources": [
        {
          "domain": "bbc.com",
          "url": "https://www.bbc.com/article-about-india"
        }
      ],
      "summary": "The article is mostly accurate but contains one factual error about India's number of states."
    }
    """
    prompt_template = f"""
You are a fact-checking expert. Carefully read the following news article and determine its factual accuracy.

Instructions:
1. Identify the main claims or statements made in the article.
2. Cross-check these claims against publicly available, trusted knowledge from reputable news sources. Be extremely thorough with this step as I do not want any false claims from your side. Ensure that the sources you are checking are up to date.
3. Flag any factual errors or inconsistencies with clear explanations.
4. If the article appears accurate, state that clearly.
5. If you know that the same topic or claim has been reported by reputable news sources, list them under `supporting_sources`.

⚠️ Important Output Format (strictly follow this structure):
Return a valid JSON object with the following fields:

- verdict: "factual", "somewhat factual", or "factually incorrect"
- issues: a list of specific claims that are incorrect or misleading. For each issue, include:
  - claim: the quoted false or misleading statement
  - explanation: why it is incorrect
- supporting_sources: a list of dictionaries in the following format:
  - domain: the domain name (e.g., "bbc.com")
  - url: the full article URL **only if you are confident it exists** and it directly supports the article's claims; otherwise, just include the domain
- summary: a short 2-line explanation of the overall factual assessment

Here is the article content:

{article_text}
    """.strip()

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt_template
    )
    
    try:
        output = json.loads(response.text)
        return output
    except Exception as e:
        raise Exception("Failed to parse JSON response: " + str(e) + "\nResponse text: " + response.text)

# For local testing:
if __name__ == "__main__":
    test_article = """
    The distance from Chennai to Bangalore is 5000 km. India has 100 states and uses the dollar as its official currency.
    """
    result = check_article_factuality(test_article)
    print(json.dumps(result, indent=2))
