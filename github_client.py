import os 
import httpx
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {  "Authorization" : "token " + GITHUB_TOKEN, "Accept" : "application/vnd.github.v3+json"}

def get_diff(repo_name,pr_number):
    url = "https://api.github.com/repos/" + repo_name + "/pulls/" + str(pr_number) + "/files"
    response = httpx.get(url, headers=HEADERS)
    return response.json()


def post_comment(repo_name, pr_number, commit_sha, comment_data):
    url = "https://api.github.com/repos/" + repo_name + "/pulls/" + str(pr_number) + "/comments"
    response = httpx.post(url,headers=HEADERS, json=comment_data)
    return response.json()

def set_merge_status( repo_name, commit_sha, state, description):
    url = "https://api.github.com/repos/" + repo_name + "/statuses/" + commit_sha
    data = {"state":state,"description":description,"context":"AI PR Reviewer"}
    response = httpx.post(url, headers=HEADERS, json=data)
    return response.json()






