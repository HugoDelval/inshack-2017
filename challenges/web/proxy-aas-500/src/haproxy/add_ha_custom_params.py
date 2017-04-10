#!/usr/bin/python3
import os

with open("/etc/haproxy/haproxy.cfg") as f:
    content = f.read()

ssl_cert = os.environ.get('SSL_CERT', '')
ssl_key = os.environ.get('SSL_KEY', '')
ssl_path = "/etc/haproxy/ssl/ssl_pem"
ssl_str = ""
if ssl_cert and ssl_key:
    os.system("mkdir -p /etc/haproxy/ssl/")
    with open(ssl_path, "w") as f:
        f.write(ssl_cert + "\n" + ssl_key)
    ssl_str = "ssl crt " + ssl_path
content = content.format(custom_headers=os.environ['CUSTOM_HEADERS'],
                         listen_port=os.environ['LISTEN_PORT'],
                         backend1=os.environ['BACKEND1'],
                         backend2=os.environ['BACKEND2'],
                         ssl_cert=ssl_str
                         )

with open("/etc/haproxy/haproxy.cfg", "w") as f:
    f.write(content)
