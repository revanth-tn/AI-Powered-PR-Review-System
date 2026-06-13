import re

def count_issues(text):
    high=len(re.findall("high",text,re.IGNORECASE))
    medium=len(re.findall("medium",text,re.IGNORECASE))
    low=len(re.findall("low",text,re.IGNORECASE))
    return high,medium,low

def calculate_score(text):
    high, medium, low = count_issues(text)
    score=100
    score-=high*10
    score-=medium*5
    score-=low*2
    return max(0,score)

def score_all_reviews(bugs_text, security_text, standards_text, tests_text, architecture_text):
    bugs=calculate_score(bugs_text)
    security=calculate_score(security_text)
    standards=calculate_score(standards_text) 
    tests=calculate_score(tests_text) 
    architecture=calculate_score(architecture_text)
    return ({"bugs":bugs,"security":security,"standards":standards,"tests":tests,"architecture":architecture})