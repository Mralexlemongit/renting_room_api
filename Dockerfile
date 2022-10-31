FROM python:3.9-slim-bullseye
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .