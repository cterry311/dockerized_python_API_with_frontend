FROM python

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn

RUN pip install pymongo

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]