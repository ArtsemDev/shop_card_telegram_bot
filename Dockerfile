FROM python:3.11.6-alpine3.18

WORKDIR /bot

COPY . /bot

RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt
