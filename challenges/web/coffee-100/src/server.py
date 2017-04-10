from flask import Flask, session, request, Response,make_response
import os
from datetime import datetime
from functools import wraps

timePouringCoffeeMin = 16
timePouringCoffeeMax = 18

timePouringMilkMin = 4
timePouringMilkMax = 7

app = Flask(__name__)
"""
    Session status:
    0 -> Pourring coffee
    1 -> Coffee served
    2 -> Pouring milk
    3 -> Ready
"""

def check_auth(username, password):
    return username == 'Coffee_Machine' and password == 'Coffee_Password'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response('You need to login.',401,{'WWW-Authenticate': 'Basic realm="Login Required"'})
        resp = make_response(f(*args, **kwargs))
        resp.headers['Accept-Additions'] = 'milk-type;syrup-type;sweetener-type;spice-type'
	resp.headers['Content-Type'] = 'message/coffeepot'
        return resp
    return decorated

@app.route('/',methods=['GET','POST'])
def main():
    return "Coffee machine server.",200

@app.route('/teapot', methods=['GET','BREW', 'POST','WHEN'])
@requires_auth
def teapot():
    return "I'm a teapot", 418

@app.route('/coffee', methods=['GET'])
@requires_auth
def get():
    if 'status' in session and session['status'] == 1:
        return "Your coffee is ready but you don't have milk in it.",406
    if 'status' in session and session['status'] == 3:
        if 'milk' not in session or 'syrup' not in session:
            return 'Not acceptable',406
        if session['milk'] != "Half-and-half":
            return "Your coffee is ready but you didn't put the right milk-type.",200
        if session['syrup'] == '':
            return "Your coffee is ready but you didn't put syrup in it.",200
        if session['syrup'] != 'Raspberry':
            return "Your coffee is ready but you didn't put the right syrup-type.",200
        return 'Here is your coffee: INSA{April_Fool_of_Coffee_Machine}',200
    else:
        session.clear()
        return 'Not acceptable',406

@app.route('/coffee', methods=['BREW','POST'])
@requires_auth
def brew():
    d = request.data.lower()
    if 'content-type' in request.headers and request.headers['content-type'] == "message/coffeepot":
        if d == "start":
            #Start coffee
            session['start'] = datetime.now()
            session['status'] = 0
            session['milk'] = "" if 'milk-type' not in request.headers else request.headers['milk-type']
            session['syrup'] = "" if 'syrup-type' not in request.headers else request.headers['syrup-type']
            return 'Starting to serve coffee',200

        elif d == "stop":
            #Stop pouring coffee
            if 'status' not in session or session['status'] != 0:
                session.clear()
                return 'Not acceptable',406

            pouring_duration = (datetime.now() - session['start']).total_seconds()

            if timePouringCoffeeMin < pouring_duration < timePouringCoffeeMax:
                session['status'] = 1
                return 'Coffee machine is stopped. You can now pour the milk.',200
            elif pouring_duration < timePouringCoffeeMin:
                session.clear()
                return "Your coffee was not ready, try again!",200
            else:
                session.clear()
                return "Coffee overflow, try again!",200

        elif d == "milk":
            if 'status' not in session or session['status'] != 1:
                session.clear()
                return 'Not acceptable',406

            session['start'] = datetime.now()
            if session['milk'] == "":
                return "You didn't set the milk type",406
            session['status'] = 2
            return 'Starting to poor milk',200

        elif d == "help" or d == "info":
            return 'Available commands: info, start, stop, milk',200
        else:
            return 'Not acceptable',406

    elif 'content-type' in request.headers and request.headers['content-type'] == "application/coffee-pot-command":
        return 'Not Implemented',501
    else:
        return 'Wrong Content-type',406

@app.route('/coffee', methods=['WHEN'])
@requires_auth
def when():
    #Stop pouring milk
    if 'status' not in session or session['status'] != 2:
        session.clear()
        return 'Not acceptable',406

    pouring_duration = (datetime.now() - session['start']).total_seconds()

    if timePouringMilkMin < pouring_duration < timePouringMilkMax:
        session['status'] = 3
        return 'Milk is served.',200
    elif pouring_duration < timePouringMilkMin:
        session.clear()
        return "Not enough milk, try again!",200
    else:
        return "Milk overflow, try again!",200

@app.route('/coffee', methods=['PROPFIND'])
@requires_auth
def meta():
    #Metadata

    #Pouring coffee
    if 'status' in session and session['status'] == 0:
        pouring_duration = (datetime.now() - session['start']).total_seconds()
        if pouring_duration < timePouringCoffeeMin:
            return "Your Coffee isn't fully served yet, you can wait a little more!",200
        elif pouring_duration > timePouringCoffeeMax:
            return "Coffee overflow!",200
        else:
            return "Your Coffee is quite full, you can stop pouring it.",200

    #Pouring milk
    elif 'status' in session and session['status'] == 2:
        pouring_duration = (datetime.now() - session['start']).total_seconds()

        if timePouringMilkMin < pouring_duration < timePouringMilkMax:
            return 'There is enough milk, you can stop pouring it.',200
        elif pouring_duration < timePouringMilkMin:
            return "Not enough milk.",200
        else:
            return "Milk overflow!",200

    else:
        return "Coffee pouring time: 16 seconds\n\r Milk pouring time: beetwen 4 and 7 seconds.",200

app.secret_key = os.urandom(24)
if __name__ == "__main__":
    app.run()
