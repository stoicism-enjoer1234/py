FROM ubuntu:22.04

WORKDIR /app

COPY ./app.py /app

RUN apt -y update

RUN apt install -y python3-flask

ENTRYPOINT ["python3", "app.py"] 