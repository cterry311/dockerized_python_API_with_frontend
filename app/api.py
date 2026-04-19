import fastapi
import json
import pymongo


app = fastapi.FastAPI()

client = pymongo.MongoClient("mongodb://db:27017/")


db = client["api"]
collections = db.list_collection_names()
if "items" not in collections:
    db.create_collection("items")

items = db["items"]


def get_next_id():
    allItems = items.find()
    ids = []
    for item in allItems:
        ids.append(item["id"])
    if len(ids) == 0:
        return 1
    return max(ids) + 1


@app.get("/items")
def root():
    allItems = items.find()
    itemContent = {}
    for item in allItems:
        itemContent[item["id"]] = item["content"]
    return fastapi.responses.JSONResponse(status_code=200, content={"content": itemContent, "message": "fetched items", "success": True})


@app.get("/item/{item_id}")
def read_item(item_id: int):
    allItems = items.find()
    ids = []
    for item in allItems:
        ids.append(item["id"])
    if item_id not in ids:
        return fastapi.responses.JSONResponse(status_code=404, content={"message": "Item not found", "success": False})
    else:
        ithItem = items.find_one({"id": item_id})["content"]
        return fastapi.responses.JSONResponse(status_code=200, content={"content": ithItem, "message": "fetched item", "success": True})


@app.post("/items")
def create_item(content: dict):
    item_id = get_next_id()
    items.insert_one({"id": item_id, "content": content})
    return fastapi.responses.JSONResponse(status_code=200, content={"item_id": item_id, "message": "pushed item", "success": True})

@app.put("/item/{item_id}")
def update_item(item_id: int, content: dict):
    allItems = items.find()
    ids = []
    for item in allItems:
        ids.append(item["id"])
    if item_id not in ids:
        return fastapi.responses.JSONResponse(status_code=404, content={"message": "Item not found"})
    else:
        items.update_one({"id": item_id}, {"$set": {"content": content}})
        return fastapi.responses.JSONResponse(status_code=200, content={"message": "updated item", "success": True})

@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    allItems = items.find()
    ids = []
    for item in allItems:
        ids.append(item["id"])
    if item_id not in ids:
        return fastapi.responses.JSONResponse(status_code=404, content={"message": "Item not found", "success": False})
    else:
        items.delete_one({"id": item_id})
        return fastapi.responses.JSONResponse(status_code=200, content={"message": "deleted item", "success": True})

# backend-api is what I called the image