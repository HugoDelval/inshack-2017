FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && DEBIAN_FRONTEND=noninteractive apt-get install -yq python3 python3-pip cron mysql-server python3-ruamel.yaml python3-flask sudo nginx-full uwsgi uwsgi-plugin-python3 && \
    pip3 install PyMySQL
RUN useradd dishwasher && \
    mkdir /app && \
    strings /dev/urandom | grep -o "[[:alnum:]]" | head -n 40 |/usr/bin/tr -d "\n" > /app/secret.txt
ADD . /app
ADD nginx_conf /etc/nginx/sites-available/dishwasher
ADD uwsgi_conf /etc/uwsgi/apps-available/dishwasher.ini

WORKDIR /app
RUN ln -s /etc/nginx/sites-available/dishwasher /etc/nginx/sites-enabled/dishwasher && \
    rm -rf .gitignore .idea/ Readme.md Dockerfile __pycache__/ && \
    touch /var/log/nginx/error.dishwasher.log && \
    mv start.sh / && chmod 700 /start.sh && \
    chmod 400 empty_table.py && \
    chmod 500 yaml_load_dump.sh && \
    chmod 444 yaml_load_dump.py && \
    echo -e '[client]\nuser=flag\npassword="the real flag (deleted for security reasons)"' >> .my.cnf && \
    # echo "dishwasher ALL = (root) NOPASSWD: /app/yaml_load_dump.sh" >> /etc/sudoers && \
    echo "*/2 * * * * root cd /app && python3 empty_table.py" >> /etc/crontab && \
    echo >> /etc/crontab && \
    sed -i 's/www-data/dishwasher/' /etc/nginx/nginx.conf

CMD mysql -uflag -pINSA{always_l00k_for_processes} dishwasher & \
    /start.sh

