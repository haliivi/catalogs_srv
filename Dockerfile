FROM python:3.11.0-alpine AS base
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Barnaul
RUN apk update
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
