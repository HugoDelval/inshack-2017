FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-flask python3-pip language-pack-fr
RUN mkdir /app
ADD . /app
RUN useradd smartsensors
RUN pip3 install flask-responses requests
RUN locale-gen "fr_FR.UTF-8"
ENV LANG="fr_FR.UTF-8" LANGUAGE="fr_FR:fr" LC_ALL="fr_FR.UTF-8"
RUN dpkg-reconfigure locales

USER smartsensors
CMD cd /app && python3 run.py
