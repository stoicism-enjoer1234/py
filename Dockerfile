FROM ubuntu:22.04

WORKDIR /flask-app

COPY ./flask-app-v1.1.py /flask-app

RUN apt -y update

RUN apt install -y python3-flask

RUN apt install -y python3-pika

RUN apt install -y python3-jsonschema

ENTRYPOINT ["python3", "flask-app-v1.1.py"] 