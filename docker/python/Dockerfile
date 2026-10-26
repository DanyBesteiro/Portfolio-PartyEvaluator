FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY docker/python/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .