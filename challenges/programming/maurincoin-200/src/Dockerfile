FROM ubuntu:latest

RUN apt-get update && apt-get install -y python python-flask python-crypto
RUN mkdir /app
ADD . /app
RUN useradd maurincoin

USER maurincoin
CMD cd /app && python server_v2.py
