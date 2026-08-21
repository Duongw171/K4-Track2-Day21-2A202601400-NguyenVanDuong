import urllib.request
import json

print("=== 1. TEST HEALTHZ ===")
req1 = urllib.request.Request("http://localhost:8080/healthz")
with urllib.request.urlopen(req1) as res:
    print(res.read().decode())

print("\n=== 2. TEST SCORE (Low Income Sample) ===")
payload1 = json.dumps({"features": [60, 2, 5, 2, 4, 0, 1, 0, 0, 45]}).encode()
req2 = urllib.request.Request("http://localhost:8080/score", data=payload1, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req2) as res:
    print(res.read().decode())

print("\n=== 3. TEST SCORE (High Income Sample) ===")
payload2 = json.dumps({"features": [28, 2, 14, 2, 11, 0, 1, 0, 0, 45]}).encode()
req3 = urllib.request.Request("http://localhost:8080/score", data=payload2, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req3) as res:
    print(res.read().decode())
