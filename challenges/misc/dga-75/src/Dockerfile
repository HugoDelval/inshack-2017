FROM node:boron

RUN apt-get update && apt-get install -y cron
RUN echo "*/10 * * * * root rm -f /usr/src/app/public/*.png" >> /etc/crontab
RUN echo '#' >> /etc/crontab

RUN useradd dga
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json /usr/src/app/
RUN npm install
RUN npm install -g phantomjs-prebuilt

COPY . /usr/src/app
RUN chown dga:dga /usr/src/app/public  -R

CMD service cron restart && su -c "node index.js" dga
