FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
        libfreetype6-dev \
        libjpeg62-dev \
        libpng12-dev \
        nginx \
        php7.0 php7.0-fpm php7.0-gd

RUN mkdir /usr/src/generation/ && \
    mkdir -p /var/www/captcha-image && \
    chown www-data:www-data /usr/src/generation/ -R && \
    chown www-data:www-data /var/www/captcha-image/ -R

USER www-data
COPY captcha-generation.php /usr/src/generation/
COPY font.ttf /usr/src/generation
WORKDIR /usr/src/generation
RUN mkdir captchas && \
    php ./captcha-generation.php
ADD web/ /var/www/captcha-image/

USER root
COPY nginx.server /etc/nginx/sites-available/captcha-image
RUN ln -s /etc/nginx/sites-available/captcha-image /etc/nginx/sites-enabled/captcha-image && \
    rm /etc/nginx/sites-enabled/default
CMD service php7.0-fpm start && service nginx restart && tail -f /var/log/nginx/error.log
