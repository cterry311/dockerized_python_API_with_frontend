from dotenv import load_dotenv
import os
import requests
import fastapi
import json
load_dotenv()


def fetchResponse(prompt, doingHousing=False):
    context = []
    if doingHousing:
        context.append({
            "role":"system",
            "content": '''
            you are a housing price predictor, you will predict housing prices based on user input. you will get input from the user in json format
            you will respond in json format, and example reply is as follows '{"price": 20000, "confidence":0.6}', you will always respond with the fields price, and confidence. each is a numerical value, where price is the value of the home, and confidence is a float between 0 and 1.
            you will not respond in anything other than a json format and will only reply with the housing price predictions
            '''
        })
    context.append({
        "role":"user",
        "content": prompt
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }
    body = {
        "model": "ai/gemma4:E4B",
        "messages": context
    }
    response = requests.post("http://localhost:12434/engines/llama.cpp/v1/chat/completions", headers=headers, json=body)
    content = response.json()
    message = content["choices"][0]["message"]["content"]
    print(message)
    return message

app = fastapi.FastAPI()

@app.post("/chat")
def chat(message: str):
    return fetchResponse(message)


@app.post("/housing")
def housing(information: object):
    json_str = json.dumps(information)
    model_response = fetchResponse(json_str, doingHousing=True)
    try:
        return json.load(model_response)
    except(json.decoder.JSONDecodeError, TypeError):
        return fastapi.responses.JSONResponse(status_code=500, content={"message": "model responded with non json", "success": False})