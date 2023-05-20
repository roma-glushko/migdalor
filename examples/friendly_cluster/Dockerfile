FROM python:3.10.11-alpine3.16 as base

ENV PYTHONPATH="/src/:$PYTHONPATH"

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -r requirements.txt

COPY ./cluster /src/cluster
