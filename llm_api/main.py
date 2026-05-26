from dotenv import load_dotenv
import os
import requests
import fastapi
import json
load_dotenv()


def fetchResponse(context, doingHousing=False):
    if doingHousing:
        prompt = context
        context = []
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
    response = requests.post("http://host.docker.internal:12434/engines/llama.cpp/v1/chat/completions", headers=headers, json=body)
    if response.status_code != 200:
        print(response.text)
        return {"ok": False, "message":"something went wrong with the request", "error": response.json()}
    content = response.json()
    message = content["choices"][0]["message"]["content"]
    print(message)
    return {"ok": True, "message": message}
# I used AI to help me troubleshoot the code, it helped me figure out that I could not use localhost for the request because it was inside of a docker container instead of running locally

app = fastapi.FastAPI()

@app.post("/chat")
def chat(context: object = fastapi.Body()):
    print("hit route")
    print(context)
    response = fetchResponse(context)
    if response["ok"]:
        return {"ok": True, "message": response["message"]}
    else:
        return fastapi.responses.JSONResponse(response, status_code=500)


@app.post("/housing")
def housing(information: object = fastapi.Body()):
    json_str = json.dumps(information)
    model_response = fetchResponse(json_str, doingHousing=True)
    print("predicted housing")
    print(model_response)
    if not model_response["ok"]:
        return fastapi.responses.JSONResponse(model_response, status_code=500)
    try:
        return fastapi.responses.JSONResponse(json.loads(model_response["message"]))
    except(json.decoder.JSONDecodeError, TypeError):
        return fastapi.responses.JSONResponse(status_code=500, content={"message": "model responded with non json", "success": False})