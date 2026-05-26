import requests
import os
import dotenv
dotenv.load_dotenv()

context = [
    {
        "role":"user",
        "content":"in one sentance, what is docker"
    }
]
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}
body = {
        "model": "ai/gemma4:E4B",
        "messages": context
}

response = requests.post("http://localhost:12434/engines/llama.cpp/v1/chat/completions", headers=headers, json=body)
if response.status_code != 200:
    print(response.text)
else:
    print(response.json())