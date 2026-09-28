import urllib.request
import json

def add_patient(name, email):
    url = "http://localhost:8081/api/patients"
    data = json.dumps({"name": name, "email": email}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as f:
            print(f"Added {name}: {f.status} {f.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error adding {name}: {e}")

add_patient("Patient1", "p1@a.com")
add_patient("Patient2", "p2@a.com")
add_patient("Patient3", "p3@a.com")
