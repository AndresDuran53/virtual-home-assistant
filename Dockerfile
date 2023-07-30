# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV TZ="America/Costa_Rica"

WORKDIR /gptAssistant

COPY requirements_docker.txt requirements_docker.txt
RUN pip3 install -r requirements_docker.txt

COPY . .

CMD [ "python3", "virtualHomeAssistant/main_docker.py"]
