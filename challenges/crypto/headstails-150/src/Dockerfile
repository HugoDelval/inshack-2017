FROM ubuntu:latest

RUN apt-get update && apt-get install -y python
RUN useradd headstails
RUN mkdir /app
ADD headstails.py /app/

USER headstails
CMD /app/headstails.py
