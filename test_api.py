import requests

# Add patient 1
print("Adding patient 1...")
r1 = requests.post("http://localhost:8081/api/patients", json={"name": "Alice", "email": "alice@test.com"})
print(r1.status_code, r1.text)

# Add patient 2
print("Adding patient 2...")
r2 = requests.post("http://localhost:8081/api/patients", json={"name": "Bob", "email": "bob@test.com"})
print(r2.status_code, r2.text)

# Get all patients
print("Getting all patients...")
r3 = requests.get("http://localhost:8081/api/patients")
print(r3.status_code, r3.text)
