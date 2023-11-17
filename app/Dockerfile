# FROM tiangolo/uvicorn-gunicorn:python3.10
FROM python:3.10.1-slim

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000" , "--reload"]