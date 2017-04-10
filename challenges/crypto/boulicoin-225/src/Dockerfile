FROM ubuntu:latest

RUN apt-get update && apt-get install -y python python-flask python-crypto
RUN mkdir /app
ADD . /app
RUN useradd boulicoin

USER boulicoin
CMD cd /app && python server_v1.py
