import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def review_security(diff):
    prompt="You are a security code reviewer. Review the following code diff and find security issues like hardcoded secrets, unsafe SQL queries, missing auth checks, exposed tokens, bad CORS config. For each issue found return: file name, line number, severity (HIGH/MEDIUM/LOW), and a clear message explaining the issue.\n\nCode diff:\n" + diff
    response = model.generate_content(prompt)
    return response.text


