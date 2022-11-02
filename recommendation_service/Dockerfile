FROM python:3.11-slim

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8080