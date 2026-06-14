from fastapi import FastAPI, Request
import hmac, hashlib, os
from dotenv import load_dotenv

load_dotenv()

from database import save_pull_request, save_comment, update_pr_scores
from github_client import get_diff, post_comment, set_merge_status
from scorer import score_all_reviews
from validator import validate_reply
from reviewers.bugs import review_bugs
from reviewers.security import review_security
from reviewers.standards import review_standards
from reviewers.tests import review_tests
from reviewers.architecture import review_architecture

app=FastAPI()

WEBHOOK_SECRET=os.getenv("WEBHOOK_SECRET")


def verify_signature(payload,signature):
    secret = WEBHOOK_SECRET.encode()
    mac=hmac.new(secret, payload, hashlib.sha256)
    return hmac.compare_digest("sha256=" + mac.hexdigest(), signature)

print("Webhook hit")
@app.post("/webhook")
async def webhook(request:Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(body, signature):
        return {"error":"invalid signature"}
    
    data = await request.json()
    action = data.get("action")
    print("Webhook action:", action)
    pr = data.get("pull_request")
    repo_name = data["repository"]["full_name"]
    pr_number = pr["number"]
    pr_title = pr["title"]

    author = pr["user"]["login"]
    commit_sha = pr["head"]["sha"]

    if action == "opened" or action == "synchronize":
        pr_id=save_pull_request(repo_name, pr_number, pr_title, author)
        diff=get_diff(repo_name, pr_number)
        bugs_review = review_bugs(diff)
        security_review = review_security(diff)
        standards_review = review_standards(diff)
        tests_review = review_tests(diff)
        architecture_review = review_architecture(diff)

        scores = score_all_reviews(
            bugs_review,
            security_review,
            standards_review,
            tests_review,
            architecture_review
        )

        comment_body = f"AI Review Complete\nBugs: {scores['bugs']}\nSecurity: {scores['security']}\nStandards: {scores['standards']}\nTests: {scores['tests']}\nArchitecture: {scores['architecture']}"

        post_comment(repo_name, pr_number, commit_sha, {"body": comment_body})

        update_pr_scores(
            pr_id,
            scores["bugs"],
            scores["security"],
            scores["tests"],
            scores["architecture"]
        )

        set_merge_status(repo_name, commit_sha, "success")

    return {"status": "ok"}
         

#testing this ptoject

########