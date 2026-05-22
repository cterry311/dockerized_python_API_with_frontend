FROM python:3.14-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn requests python-dotenv

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]