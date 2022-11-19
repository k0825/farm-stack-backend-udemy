FROM python:3.9-slim

WORKDIR /workspace
COPY requirements.txt .

RUN apt-get update && apt-get install -y git

RUN pip install -U pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt