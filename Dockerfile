FROM tiangolo/uvicorn-gunicorn:python3.10

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./models /models

COPY ./app /app
