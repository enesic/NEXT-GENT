import urllib.request
import json
import urllib.parse
from urllib.error import HTTPError

url = "http://localhost:8001/api/v1/helpdesk/chat"
headers = {
    "Content-Type": "application/json"
}
data = {
    "message": "Merhaba",
    "context": {
        "page": "landing"
    }
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")

try:
    print(f"Sending POST to {url}...")
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response Body: {response.read().decode('utf-8')}")
except HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    print(f"Error Body: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
