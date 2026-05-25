FROM python:3.14-slim

WORKDIR /app

RUN pip install fastapi uvicorn requests python-dotenv

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]