FROM node:boron

RUN apt-get update && apt-get install -y p7zip-full espeak sox

RUN useradd audiocaptcha
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json /usr/src/app/
RUN npm install

COPY generateAudioFiles.py /usr/src/app/
RUN python generateAudioFiles.py
RUN 7z a -ptoto audioFiles.zip audioFiles

COPY generateCaptchaFiles.py /usr/src/app/
RUN python generateCaptchaFiles.py

COPY . /usr/src/app
RUN mkdir /usr/src/app/public
RUN chown audiocaptcha:audiocaptcha /usr/src/app/public  -R

CMD su -c "node index.js" audiocaptcha
