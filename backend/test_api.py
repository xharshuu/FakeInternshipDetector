import urllib.request
import urllib.parse
import json

URL = "http://127.0.0.1:5001/check"

# A completely obvious fake job description
fake_job = """
URGENT HIRING!!! Data Entry Clerk (WORK FROM HOME)
Salary: $900/week! No experience needed!
Equipment will be provided, but you must first send a $200 security deposit for the Apple MacBook Pro via Zelle or CashApp.
Once payment is received, we will send tracking info.
Start today. Only 2 spots left!!!
Don't miss this opportunity.
"""

# A normal job description
legit_job = """
Software Engineering Intern - Summer 2026
Google is looking for a Software Engineering Intern to join our Cloud team.
Requirements:
- Currently pursuing a BS/MS in Computer Science or related field.
- Experience with Python, Java, or C++.
- Strong problem-solving skills.
Location: Sunnyvale, CA
Please apply through the official careers page.
"""

def make_request(text):
    data = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return str(e)

def test_api():
    print("Testing Fake Job:")
    print(make_request(fake_job))
    
    print("\nTesting Legit Job:")
    print(make_request(legit_job))

if __name__ == "__main__":
    test_api()
