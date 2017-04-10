FROM node:onbuild

EXPOSE 12345
ENV PORT 12345

RUN apt-get update
RUN apt-get -y install netcat ucspi-tcp
WORKDIR /usr/src/app
RUN ["npm","link","console-png"]
RUN ["rm","Dockerfile"]
RUN ["rm","package.json"]
RUN ["rm","Readme.md"]
CMD tcpserver -v -c 50 -t 3 0.0.0.0 12345 ./chall.sh
