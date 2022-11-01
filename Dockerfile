FROM python:3.9-slim-bullseye
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY ./project/ /code/

RUN python -m pip install -r requirements.txt
