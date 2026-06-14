import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
supabase=create_client(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))

def save_pull_request(repo_name, pr_number,pr_title,author):
    result=supabase.table("pull_requests").insert({"repo_name":repo_name,"pr_number":pr_number,"pr_title":pr_title,"author":author,"status":"open"}).execute()
    return result.data[0]["id"]

def save_comment(pr_id, reviewer_type, file_path, line_number, severity, message, suggestion):
    result=supabase.table("review_comments").insert({"pr_id":pr_id,"reviewer_type":reviewer_type,"file_path":file_path, "line_number":line_number, "severity":severity, "message":message, "suggestion":suggestion,"status":"open"}).execute()
    return result.data[0]["id"]

def save_reply( comment_id, reply_text, is_valid, validation_reason):
    supabase.table("developer_replies").insert({"comment_id":comment_id,"reply_text":reply_text, "is_valid":is_valid, "validation_reason":validation_reason}).execute()

def get_open_comments(pr_id):
    result = (supabase.table("review_comments").select("*").eq("pr_id",pr_id).eq("status","open")).execute()
    return result.data

def resolve_comments(comment_id):
    result = (supabase.table("review_comments").update({"status":"resolved"}).eq("id",comment_id)).execute()

def update_pr_scores(pr_id, code_quality, security, testing, maintainability):
    result = (supabase.table("pull_requests").update({"code_quality_score":code_quality, "security_score":security, "testing_score":testing, "maintainability_score":maintainability}).eq("id",pr_id)).execute()