import requests


response = requests.get("http://localhost:8001/health")
json_content = response.json()
if response.status_code != 200:
    print("Error: ", json_content)
else:
    print("All healthy here!!")
