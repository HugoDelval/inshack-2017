FROM ubuntu:latest

RUN apt-get update && apt-get install -y nginx php-fpm
RUN sed -i -- 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/g' /etc/php/7.0/fpm/php.ini
RUN mkdir -p /var/www/html/
ADD . /var/www/html/
RUN rm /var/www/html/Dockerfile
RUN mv /var/www/html/nginx_conf /etc/nginx/sites-available/easyhtml
RUN ln -s /etc/nginx/sites-available/easyhtml /etc/nginx/sites-enabled
CMD service nginx restart && \
    service php7.0-fpm start && \
    tail -f /var/log/nginx/error.easyhtml.log
