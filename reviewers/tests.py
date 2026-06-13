import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def review_tests(diff):
    prompt = f"""
You are an expert senior software engineer and test reviewer.

Review the following code changes and find testing-related issues only.

Look specifically for:

1. Missing test cases
2. Untested edge cases
3. Hardcoded test data
4. Tests that do not assert anything meaningful
5. Missing mocks for external services

Code changes:

{diff}

Return your review in this format:

Issue:
Category:
File:
Line:
Severity: low / medium / high
Explanation:
Suggested fix:
"""
    response = model.generate_content(prompt)
    return response.text


