# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV TZ="America/Costa_Rica"

WORKDIR /gptAssistant

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "virtualHomeAssistant/assistant.py"]

