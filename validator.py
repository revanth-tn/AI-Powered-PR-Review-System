import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def validate_reply(original_issue,developer_reply):
    prompt = f"""
You are a code review validator.

The original issue is:

{original_issue}

The developer's reply is:

{developer_reply}

Decide if the developer's reply genuinely fixes or addresses the original issue.

Return only in this format:

is_valid: true/false
reason: explanation
"""
    
    response=model.generate_content(prompt)
    return response.text
