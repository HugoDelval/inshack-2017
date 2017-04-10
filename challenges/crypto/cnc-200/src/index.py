#!/usr/bin/python3
import os, base64, json
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)
with open("secret.txt") as f:
    app.secret_key = f.read()
with open("flag.txt") as f:
    FLAG = f.read()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
BS = AES.block_size
key = Random.new().read(BS)
obj = AES.new(key)


def decrypt(payload):
    unpad = lambda s: s[0:-ord(s[-1])]
    json_str_padded = obj.decrypt(base64.b64decode(payload))
    json_str = unpad(json_str_padded.decode('utf-8'))
    return json.loads(json_str)


def encrypt(data):
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    json_str = json.dumps(data)
    payload = obj.encrypt(pad(json_str))
    return base64.b64encode(payload).decode('utf-8')


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    localisation = db.Column(db.String(120))
    model = db.Column(db.String(120))
    bw = db.Column(db.Integer)
    is_cnc = db.Column(db.Boolean, default=False)  # Sorry :p

    def __init__(self, login, password, localisation, model, bw):
        self.login = login
        self.password = password
        self.localisation = localisation
        self.model = model
        self.bw = bw

    def serialize(self):
        return [
            ('model', self.model),
            ('localisation', self.localisation),
            ('password', self.password),
            ('is_cnc', self.is_cnc),
            ('bw', self.bw),
            ('login', self.login),
        ]

    def get_cookie(self):
        return encrypt(self.serialize())


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        try:
            the_bot = Bot.query.filter_by(login=request.form['login'], password=request.form["password"]).first()
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('data', the_bot.get_cookie())
            flash("You've been successfully logged in.")
            return resp
        except:
            flash("Error occurred while logging in.")
            return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        expected_params = ["login", "password", "localisation", "model", "bw"]
        try:
            new_bot = Bot(**{i: request.form[i] for i in expected_params})
            db.session.add(new_bot)
            db.session.commit()
            flash("You've been successfully registered. Please login now")
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash("Error while registering. Maybe the user already exists? Please try again.")
            return render_template('register.html')


@app.route("/profile", methods=["GET"])
def profile():
    try:
        payload = request.cookies.get('data')
        bot = decrypt(payload)
        if any(map(lambda x: x[0] == "is_cnc" and x[1]==True, bot)):
            bot.append(("flag", FLAG))
        return render_template('profile.html', bot=bot)
    except:
        flash("Error while trying to decrypt session data. Are you sure you are logged in?")
        return redirect(url_for("login"))


@app.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('data', '', expires=0)
    flash("You've been successfully logged out.")
    return resp


if __name__ == '__main__':
    app.run("0.0.0.0")
