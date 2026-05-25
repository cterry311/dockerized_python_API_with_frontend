FROM pytorch/pytorch:latest

WORKDIR /app

RUN pip install fastapi uvicorn requests

COPY . /app

CMD ["uvicorn", "model_api:app", "--host", "0.0.0.0", "--port", "8001"]