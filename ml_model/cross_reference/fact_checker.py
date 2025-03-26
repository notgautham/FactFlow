import os
from dotenv import load_dotenv
from google import genai

# ✅ Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("❌ GEMINI_API_KEY not found in .env file")

# ✅ Initialize Gemini client
client = genai.Client(api_key=api_key)

# ✅ Editable article text
article_text = """
Trump top aide takes ‘full responsibility’ for military chat leak as US President defends ‘good man’
Mike Waltz accepted responsibility for making the Signal group, though he continued to deflect blame, insulted the editor-in-chief of the Atlantic and said he couldn’t explain how the mistake had occurred.
By: Express Web Desk
March 26, 2025 16:54 IST
Newsguard
clock_logo3 min read
facebook
twitter
whatsapp
Reddit
Newsguard
Mike Waltz Security leak White House National Security Adviser Mike Waltz listens to a question from a reporter in the James Brady Press Briefing Room at the White House, in Washington, Feb. 20, 2025. (AP Photo/Alex Brandon, file)
A day after what Donald Trump termed as “the only glitch in two months”, US National Security Adviser, Mike Waltz, said he took full responsibility for leak of military plans in a Signal chat.

“I take full responsibility. I built the group. My job is to make sure everything is coordinated,” Waltz said in an interview with Fox News, in which he conceded: “it’s embarrassing”.

Waltz’s comments came one day after Jeffrey Goldberg, editor-in-chief of the Atlantic, revealed that he was added to a group on Signal, a private messaging app, that included vice-president JD Vance, defense secretary Pete Hegseth, secretary of state Marco Rubio and other high-profile figures discussing “operational details” of US airstrikes on Houthis in Yemen.

Waltz, speaking to Fox News’ Laura Ingraham, admitted to creating the chat but deflected blame, insulted Goldberg, and insisted he didn’t know how the mistake occurred. “It’s embarrassing, yes. We’re going to get to the bottom of it,” he said, adding that he was consulting with Elon Musk: “We’ve got the best technical minds looking at how this happened.”

Also read | Emojis, European ‘freeloading’ and JD Vance’s Yemen ‘mistake’ alert – takeaways from US security leak
When asked “what staffer is responsible” for adding Goldberg to the Signal group, Waltz said: “A staffer wasn’t responsible. I take full responsibility. I built the group. My job is to make sure everything is coordinated.”

Pressed on how Goldberg’s number ended up in the group, Waltz said: “Have you ever had somebody’s contact that shows their name and then you have somebody else’s number there? … Of course I didn’t see this loser in the group. It looked like someone else.” He also floated an unsubstantiated theory that Goldberg may have “deliberately” ended up in the chat but failed to provide any evidence.



Trump, meanwhile, added to the confusion in a separate Newsmax interview, appearing to contradict Waltz’s claim that no staffer was responsible. “We believe … somebody that was on the line, with permission, somebody that … worked with Mike Waltz at a lower level, had Goldberg’s number or call through the app, and somehow this guy ended up on the call.” His remarks further muddied the situation, given that Goldberg was added to a text chat, not a call.

mail logo
Daily newsletter specially tailored for Indian Express global readers

Enter Your Email
 
Trump previously defended Waltz, saying he was a “good man” who “learned a lesson”, and also downplayed the incident, saying the leak was “the only glitch in two months, and it turned out not to be a serious one”.
"""


# ✅ Editable prompt
prompt_template = f"""
You are a fact-checking expert. Carefully read the following news article and determine its factual accuracy.

Instructions:
1. Identify the main claims or statements made in the article.
2. Cross-check these claims against publicly available, trusted knowledge from reputable news sources. Be extremely thorough with this step as I do not want any false claims from your side. Ensure that the sources you are checking are upto date.
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
"""


# ✅ Send request to Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt_template
)

# ✅ Print result
print(response.text)
