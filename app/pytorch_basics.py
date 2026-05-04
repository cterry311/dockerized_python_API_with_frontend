import torch
import torch.nn as nn
import numpy
import sklearn.datasets as datasets
import sklearn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import os

def gradient_demo():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    basic_tensor = torch.tensor([1.,2.,3.], requires_grad=True).to(device)
    print(basic_tensor)

    basic_tensor_out = basic_tensor * 3 + 5

    total = basic_tensor_out.sum()
    total.backward()


    print(basic_tensor.grad)
    # I used AI to assist me with figuring out exactly how to get the gradient for a tensor, it turns out that you need to call .backward() on a scaler and use intermediate tensors


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

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data, labels):
        # one_hot_labels = np.zeros((len(labels), 3))
        # one_hot_labels[np.arange(len(labels)), labels] = 1
        data = torch.from_numpy(data).float()
        labels = torch.from_numpy(labels)
        # one_hot_labels = torch.from_numpy(one_hot_labels).float()
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)          # total number of samples

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]  # I used AI to write this class for me


def loadData():

    dataset = datasets.load_iris()
    trainX, testX, trainY, testY = sklearn.model_selection.train_test_split(dataset.data, dataset.target, test_size=0.2)


    trainset = MyDataset(trainX, trainY)
    testset = MyDataset(testX, testY)


    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64,
                                              shuffle=True)


    testloader = torch.utils.data.DataLoader(testset, batch_size=64,
                                             shuffle=False)


    print("finished loading data")

    return trainloader, testloader

def trainModel():
    trainLoader, _ = loadData()
    params = [4, 10, 3]
    model = SimpleClassifier(*params)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    for epoch in range(50):
        running_loss = 0.0
        for i, data in enumerate(trainLoader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
    torch.save(model.state_dict(), 'model.pth')
    torch.save(params, 'params.pth')

def testModel():
    model = SimpleClassifier(*torch.load('params.pth'))
    model.load_state_dict(torch.load('model.pth'))
    model.eval()
    trainLoader, testLoader = loadData()
    with torch.no_grad():
        correct = 0
        total = 0
        for data in trainLoader:
            inputs, labels = data
            outputs = model(inputs)
            class_idx = torch.argmax(outputs, dim=1)
            total += labels.size(0)
            correct += (class_idx == labels).sum().item()
        print("Train Accuracy: ", correct/total)
        correct = 0
        total = 0
        for data in testLoader:
            inputs, labels = data
            outputs = model(inputs)
            class_idx = torch.argmax(outputs, dim=1)
            total += labels.size(0)
            correct += (class_idx == labels).sum().item()
        print("Test Accuracy: ", correct/total)


#trainModel()
testModel()