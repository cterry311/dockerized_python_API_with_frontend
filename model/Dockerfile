FROM pytorch/pytorch:latest

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn requests

CMD ["uvicorn", "model_api:app", "--host", "0.0.0.0", "--port", "8001"]