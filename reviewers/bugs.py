import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def review_bugs(diff):
    prompt = f"""
You are an expert senior software engineer and code reviewer.

Review the following code changes and find only real issues related to:

1. Null pointer issues
2. Edge cases
3. Race conditions
4. Unhandled exceptions
5. Broken logic

Code changes:
{diff}

Return your review in this format:

Issue:
File:
Line:
Severity: low / medium / high
Explanation:
Suggested fix:
"""
    response = model.generate_content(prompt)
    return response.text