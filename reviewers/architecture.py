import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def review_architecture(diff):
    prompt = f"""
You are an expert senior software architect and code reviewer.

Review the following code changes and find architecture/design issues only.

Look specifically for:

1. Tight coupling between modules
2. Single responsibility violations
3. Missing abstraction layers
4. Circular dependencies
5. Scalability concerns

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


