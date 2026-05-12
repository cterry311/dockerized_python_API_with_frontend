import fastapi
from typing import List

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


model = SimpleClassifier(*torch.load('params.pth'))
model.load_state_dict(torch.load('model.pth'))
model.eval()


app = fastapi.FastAPI()





@app.post("/predict")
def predict(inputs : List[float]):
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

@app.get("/health")
def health():
    print("health check")
    return {"status": "healthy", "model_loaded": model is not None, "message": "model loaded", "success": True}