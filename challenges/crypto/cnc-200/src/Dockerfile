FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3 python3-pip python3-crypto cron && \
    pip3 install flask-sqlalchemy
RUN useradd cnc && \
    mkdir /app && \
    strings /dev/urandom | grep -o "[[:alnum:]]" | head -n 40 |/usr/bin/tr -d "\n" > /app/secret.txt && \
    chown cnc:cnc /app
ADD . /app

WORKDIR /app
RUN rm -rf .gitignore .idea/ Readme.md Dockerfile user.db __pycache__/ && \
    echo "*/15 * * * * cnc cd /app && rm -f user.db && python3 init_db.py" >> /etc/crontab && \
    echo >> /etc/crontab

CMD service cron restart && \
    su -c 'python3 init_db.py && python3 index.py' cnc