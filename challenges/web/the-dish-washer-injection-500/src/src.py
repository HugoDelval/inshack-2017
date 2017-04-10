import random
import string
import subprocess

import pymysql
import base64

import re

import sys
from flask import Flask
from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from ruamel import yaml

app = Flask(__name__)
with open("secret.txt") as f:
    app.secret_key = f.read()
db = pymysql.connect("localhost", "dishwasher_user", "dishwasher_password", "dishwashers_db")


#######################
####### UTILS #########
#######################
def random_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(50)])


def select(query):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor


def insert(query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        db.commit()
        return True
    except Exception as e:
        print(e, file=sys.stderr)
        db.rollback()
        return False


class DishWasher:
    def __init__(self, id: str, name: str, brand: str, cost: int, cve: str):
        self.id = id
        self.name = name
        self.brand = brand
        self.cost = cost
        self.cve = cve


def get_new_id() -> str:
    while True:
        id = random_id()
        query = "SELECT * FROM dishwashers WHERE id='{id}'"
        nb_res = len(select(query.format(id=id)).fetchall())
        if nb_res == 0:
            return id
#######################
##### END UTILS #######
#######################


def create_dishwasher(name: str, brand: str, cost: int, cve: str) -> str:
    try:
        query = "INSERT INTO dishwashers VALUES ('{inserted_by}', '{id}', '{object}')"
        id = get_new_id()
        new_dishwasher = DishWasher(id, name, brand, cost, cve)
        if "user" in request.cookies:
            inserted_by = base64.b64decode(request.cookies["user"]).decode('utf-8')
        else:
            inserted_by = "no one :("
        if len(inserted_by) > 255:
            return ""
        for c in inserted_by:
            if c not in string.printable[:-2]:
                return ""
        if re.search(r"sleep", inserted_by, flags=re.IGNORECASE):
            return ""
        if re.search(r"benchmark", inserted_by, flags=re.IGNORECASE):
            return ""
        if re.search(r"wait", inserted_by, flags=re.IGNORECASE):
            return ""
        if insert(query.format(id=id, object=yaml.dump(new_dishwasher), inserted_by=inserted_by)):
            return id
    except Exception as e:
        print(e, file=sys.stderr)
    return ""


def fake_yaml_load(dumped):
    serialized_obj = subprocess.check_output(["sudo", "/app/yaml_load_dump.sh", dumped]).decode('utf-8')
    dishwasher_dict = yaml.safe_load(serialized_obj)
    dishwasher = DishWasher(dishwasher_dict['id'], dishwasher_dict['name'], dishwasher_dict['brand'],
                            dishwasher_dict['cost'], dishwasher_dict['cve'])
    return dishwasher


def get_dishwasher(id: str) -> (DishWasher, str):
    if not id.isalnum():
        return None, None
    try:
        query = "SELECT * FROM dishwashers WHERE id='{id}' LIMIT 1"
        res = select(query.format(id=id)).fetchone()
        if not res:
            return None, None
        dishwasher = yaml.load(res[2])
        # dishwasher = fake_yaml_load(res[2])
        return dishwasher, res[0]
    except Exception as e:
        print(e, file=sys.stderr)
        return None, None


@app.route('/')
def index():
    resp = make_response(render_template("index.html"))
    if "user" not in request.cookies:
        resp.set_cookie('user', base64.b64encode(b'user with no name'))
    return resp


@app.route('/add_dishwasher', methods=['POST'])
def add_dishwasher():
    try:
        id = create_dishwasher(request.form['name'], request.form['brand'], int(request.form['cost']), request.form['cve'])
        if id:
            flash("Dishwasher successfully added.")
            return redirect(url_for("show_dishwasher", id=id))
        else:
            flash("Error while adding dishwasher. Maybe you're a hacker?")
            return redirect('/')
    except Exception as e:
        print(e, file=sys.stderr)
        flash("Error while adding dishwasher.")
        return redirect("/")


@app.route('/dishwasher/<id>')
def show_dishwasher(id):
    res = get_dishwasher(id)
    dishwasher, inserted_by = res
    if not dishwasher:
        flash("Sorry we couldn't find dishwasher :/ Maybe it has been hacked?")
        return redirect("/")
    return render_template("dishwasher.html", dishwasher=dishwasher, added_by=inserted_by)


if __name__ == '__main__':
    # Note: to launch the application, please run these commands before:
    # apt-get install -yq python3 python3-pip cron mysql-server python3-ruamel.yaml python3-flask
    # pip3 install PyMySQL
    # mysql -uroot -p -e "CREATE DATABASE dishwashers_db;CREATE USER 'dishwasher_user'@'localhost' IDENTIFIED BY 'dishwasher_password'; GRANT INSERT, SELECT ON dishwashers_db.* TO 'dishwasher_user'@'localhost';"
    # mysql -uroot -p -e "USE dishwashers_db;CREATE TABLE dishwashers (inserted_by VARCHAR(255), id VARCHAR(255), dishwasher_object TEXT, PRIMARY KEY ( id ));"
    # python3 src.py
    try:
        app.run("0.0.0.0", debug=True)
    finally:
        db.close()
