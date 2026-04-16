import fastapi
import json

app = fastapi.FastAPI()

items : dict[int, dict] = {
    1: {"name": "Item 1", "description": "This is item 1"},
    2: {"thingy": "this is a thiny", "pointless": True},
}


def get_next_id():
    return max(items.keys()) + 1


@app.get("/items")
def root():
    return fastapi.responses.JSONResponse(status_code=200, content={"content": items, "message": "fetched items", "success": True})


@app.get("/item/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        return fastapi.responses.JSONResponse(status_code=404, content={"message": "Item not found", "success": False})
    else:
        return fastapi.responses.JSONResponse(status_code=200, content={"content": items[item_id], "message": "fetched item", "success": True})


@app.post("/items")
def create_item(content: dict):
    item_id = get_next_id()
    items[item_id] = content
    return fastapi.responses.JSONResponse(status_code=200, content={"item_id": item_id, "message": "pushed item", "success": True})

@app.put("/item/{item_id}")
def update_item(item_id: int, content: dict):
    if item_id not in items:
        return fastapi.responses.JSONResponse(status_code=404, content={"message": "Item not found"})
    else:
        items[item_id] = content
        return fastapi.responses.JSONResponse(status_code=200, content={"message": "updated item", "success": True})

@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        return fastapi.responses.JSONResponse(status_code=404, content={"message": "Item not found", "success": False})
    else:
        del items[item_id]
        return fastapi.responses.JSONResponse(status_code=200, content={"message": "deleted item", "success": True})

# backend-api is what I called the image