FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y build-essential python-dev python-pip libpcre3 libpcre3-dev

RUN pip install --upgrade pip
RUN pip install requests flask

RUN apt-get install -y nginx-full uwsgi uwsgi-plugin-python

RUN mkdir -p /var/run/coffee

ADD server.py /var/run/coffee

RUN chown -R www-data:www-data /var/run/coffee

ADD nginx_conf /etc/nginx/sites-available/coffee

ADD uwsgi_conf /etc/uwsgi/apps-available/coffee.ini
#RUN rm /etc/nginx/sites-enabled/default && rm /etc/nginx/sites-available/default
RUN ln -s /etc/nginx/sites-available/coffee /etc/nginx/sites-enabled/coffee

RUN ln -s /etc/uwsgi/apps-available/coffee.ini /etc/uwsgi/apps-enabled/coffee.ini

RUN touch /var/log/nginx/error.coffee.log

EXPOSE 8080

CMD service nginx restart && uwsgi --ini /etc/uwsgi/apps-available/coffee.ini && tail -f /var/log/nginx/error.coffee.log

