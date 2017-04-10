#!/usr/bin/env bash
cd /app
service cron restart
service mysql restart
mysql -uroot -e "CREATE DATABASE dishwashers_db;CREATE USER 'flag'@'localhost' IDENTIFIED BY 'INSA{always_l00k_for_processes}';CREATE USER 'adminuser'@'localhost' IDENTIFIED BY 'oarlkbvpamoqisjfpmqlezknovremhk';CREATE USER 'dishwasher_user'@'localhost' IDENTIFIED BY 'dishwasher_password'; GRANT INSERT, SELECT ON dishwashers_db.* TO 'dishwasher_user'@'localhost';GRANT CREATE, DELETE, INSERT ON dishwashers_db.* TO 'adminuser'@'localhost';"
mysqladmin -uroot password qsmveqveveivsdvidfdsdfidfvdsfvdov
python3 init_db.py
uwsgi --ini /etc/uwsgi/apps-available/dishwasher.ini
service nginx restart
tail -f /var/log/nginx/error.dishwasher.log
