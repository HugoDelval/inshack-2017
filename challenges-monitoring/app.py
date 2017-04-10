from flask import Flask, jsonify, request, Response
from functools import wraps
from configparser import ConfigParser
import json
import time

app = Flask(__name__)

##########################
##### Configuration ######
##########################
USERNAME = None
PASSPHRASE = None
CONFIG_FILE = 'challenge-monitoring.ini'
config = ConfigParser()
if len(config.read(CONFIG_FILE)) == 0:
    print('error: failed to load configuration file (%s)' % 'challenge-monitoring.ini')
    exit(1)
else:
    USERNAME = config['authentication']['username'].strip()
    PASSPHRASE = config['authentication']['passphrase'].strip()

##########################
##### Authentication #####
##########################
def check_auth(username, password):
    return username == USERNAME and password == PASSPHRASE


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
##########################
### End Authentication ###
##########################


@app.route('/')
def get_status():
    try:
        with open("/app/status.json") as f:
            status = json.load(f)
    except Exception as e:
        print(e)
        status = {}
    resp = jsonify(status)
    resp.status_code = 200

    return resp


@requires_auth
@app.route('/save', methods=['POST'])
def save_database():
    try:
        db = request.files['db']
        filename = "backup_" + str(int(time.time())) + '.sql'
        db.save("/backup/" + filename)
        status = {"message": "OK"}
    except Exception as e:
        status = {"message": str(e)}
    return jsonify(status)


if __name__ == "__main__":
    app.run("0.0.0.0")
