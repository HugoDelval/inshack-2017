FROM ubuntu:latest

RUN apt-get update && \
    useradd ultimateb64 && \
    mkdir /app && \
    chown ultimateb64:ultimateb64 /app -R
WORKDIR /app
USER ultimateb64
ADD flag.txt .
ADD ultimateb64 .

CMD ./ultimateb64
