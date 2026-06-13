import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def review_standards(diff):
    prompt = f"""
You are an expert senior software engineer and code quality reviewer.

Review the following code changes and find issues related to:

1. Naming conventions
2. Folder structure
3. Logging style
4. Error handling
5. Comment quality
6. Code readability

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