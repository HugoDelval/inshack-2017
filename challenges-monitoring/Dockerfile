FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-flask cron python3-requests python3-pip p7zip-full python-pip git python-requests tesseract-ocr
RUN useradd exploiter
RUN pip install Pillow numpy pwn && \
    pip3 install git+https://github.com/arthaud/python3-pwntools.git
ADD challenges /challenges
ADD challenges-monitoring/ /app
RUN mv /app/challenge-monitoring.ini.dist /app/challenge-monitoring.ini && \
    sed -i s/passphrase=/passphrase=$PASSWORD/ /app/challenge-monitoring.ini && \
    sed -i s/username=/username=$USERNAME/ /app/challenge-monitoring.ini && \
    chown exploiter:exploiter /app /challenges -R && \
    echo '*/5 * * * * exploiter bash -c "export TERM=linux && export TERMINFO=/etc/terminfo && /app/generate_status.py > /tmp/lastexploit_output 2>&1"' >> /etc/crontab && \
    echo >> /etc/crontab

CMD service cron start && \
    chown exploiter:exploiter /backup -R && \
    cd /app && \
    su -c "python3 app.py" exploiter
