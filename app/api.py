import fastapi
import json
import pymongo
import torch.nn as nn
import torch



class SimpleClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.act1 = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.act1(self.layer1(x))
        x = self.layer2(x)
        return x


model = SimpleClassifier(*torch.load('../model/params.pth'))
model.load_state_dict(torch.load('../model/model.pth'))
model.eval()


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

@app.post("/predict")
def predict(inputs: list[float]):
    '''
    iris prediction endpoint
    :param inputs: expects a list of floats of length 4, with each value representing a featuer of the iris dataset, expecteded in the order, sepal length, sepal width, petal length, petal width
    :return: a prediction of the model
    '''
    if len(inputs) != 4 or type(inputs[0]) != float:
        return fastapi.responses.JSONResponse(status_code=400, content={"message": "bad request", "success": False})
    with torch.no_grad():
        outputs = model(torch.tensor(inputs))
    return fastapi.responses.JSONResponse(
        status_code=200,
        content={"content": {
            "outputs": outputs.tolist(),
            "softmax": torch.softmax(outputs, dim=0).tolist(),
            "prediction": torch.argmax(outputs).item()
        }, "message": "prediction made", "success": True},
    )

# backend-api is what I called the image