#!/usr/bin/python3
import os
import subprocess

import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask.ext.sqlalchemy import SQLAlchemy
import requests, re
import socket

from haproxy import launch_haproxy

app = Flask(__name__)
with open("secret.txt") as f:
    app.secret_key = f.read()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
s.close()


class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now() - datetime.timedelta(minutes=3))
    port = db.Column(db.Integer, unique=True)

    def __init__(self, port):
        self.port = port


class ActionByIPAdrr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    ip = db.Column(db.String, unique=True)

    def __init__(self, ip):
        self.ip = ip


def is_valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False


def is_valid_port(port: str) -> bool:
    try:
        p = int(port)
        return 0 < p < 65536
    except:
        return False


def is_http_header(header: str) -> bool:
    m = re.match(r'\w{3,20} \w{3,200}', header)
    return m is not None


def is_valid_ssl_cert(ssl_cert: str) -> bool:
    p = subprocess.Popen(["openssl", "x509", "-text", "-noout"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    _ = p.communicate(input=ssl_cert.encode())
    return p.returncode == 0


def is_valid_ssl_key(ssl_key):
    p = subprocess.Popen(["openssl", "rsa", "-check"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    _ = p.communicate(input=ssl_key.encode())
    return p.returncode == 0


def port_is_used(port):
    return os.system("docker ps | grep '0.0.0.0:" + str(port) + "->" + str(port) + "/tcp'") == 0


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        try:
            url_recaptcha = "https://www.google.com/recaptcha/api/siteverify"
            data_recaptcha = {
                "secret": "XXX",
                "response": request.form["g-recaptcha-response"]
            }
            ip1 = request.form["ip_backend1"]
            ip2 = request.form["ip_backend2"]
            port1 = request.form["port_backend1"]
            port2 = request.form["port_backend2"]
            ssl_cert = request.form["ssl_cert"]
            ssl_key = request.form["ssl_key"]
            http_headers = request.form["http_headers"]

            ip_client = request.remote_addr
            if ip_client != "134.214.182.12":
                action = ActionByIPAdrr.query.filter_by(ip=ip_client).first()
                if action and action.timestamp > datetime.datetime.now() - datetime.timedelta(seconds=20):
                    flash("Sorry you can only launch an instance every 20s.")
                    return redirect("/")
                elif action:
                    action.timestamp = datetime.datetime.now()
                else:
                    action = ActionByIPAdrr(ip=ip_client)
                    db.session.add(action)
            if http_headers:
                http_headers = http_headers.split(";")
                for http_header in http_headers:
                    if http_header and not is_http_header(http_header):
                        flash("Invalid HTTP header")
                        return redirect('/')
            if (ssl_key and not ssl_cert) or (ssl_cert and not ssl_key):
                flash("If you want to use SSL, you need to specify both SSL private key and SSL certificate.")
                return redirect("/")
            if ssl_cert and not is_valid_ssl_cert(ssl_cert):
                flash("SSL Cert not valid")
                return redirect('/')
            if ssl_key and not is_valid_ssl_key(ssl_key):
                flash("SSL Private Key not valid")
                return redirect('/')
            if ssl_key:
                ssl = (ssl_cert, ssl_key)
            else:
                ssl = None
            if not is_valid_ip(ip1) or not is_valid_ip(ip2) or not is_valid_port(port1) or not is_valid_port(port2):
                flash("Invalid IP/PORT")
                return redirect("/")
            try:
                pswd = request.args["pswd"]
            except:
                pswd = ""
            if pswd != "zTOkNv6AIFFTFuZLKFRPTdiTCwHIpvqtBlUuY4103lS2Xf8nnX":
                r = requests.post(url_recaptcha, data=data_recaptcha)
                resp_data = r.json()
                if not resp_data.get("success", False):
                    flash("Invalid captcha")
                    return redirect("/")

            port = Port.query.filter(Port.timestamp < datetime.datetime.now() - datetime.timedelta(minutes=2, seconds=30)).first()
            if not port or port_is_used(port.port):
                flash("Sorry I couldn't find a free port, wait a bit please.")
                return redirect("/")
            port.timestamp = datetime.datetime.now()
            db.session.commit()
            launch_haproxy.launch(port.port, http_headers, ip1 + ":" + port1, ip2 + ":" + port2, ssl)
            http = "http"
            if ssl:
                http += "s"
            flash("The load balancer has been successfully launched. It will be available for 2 minutes at: " + http + "://" + my_ip + ":" + str(port.port))
        except Exception as e:
            print(e)
            flash("Error launching your proxy. Please try again.")
        return redirect('/')

if __name__ == '__main__':
    app.run()
