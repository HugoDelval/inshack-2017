FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python python-pip python-virtualenv gdb
RUN useradd lost-file && \
    mkdir /app && \
    chown lost-file:lost-file /app -R 
WORKDIR /app
USER lost-file
ADD challenge.py .
ADD run.sh .

CMD ./run.sh && rm -f ./run.sh && /bin/bash
