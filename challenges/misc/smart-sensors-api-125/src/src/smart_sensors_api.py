#!/usr/bin/env python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                       IMPORTS, GLOBALS AND MODULES INITIALIZATION
# ------------------------------------------------------------------------------------------

import uuid
import hashlib
import os
import locale
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import escape
from flask_responses import json_response
#from flask_cors import CORS
from src.utils import validator
from src.utils import ini
from src.utils import sensors
from src.utils.response import Response
from src.utils.wrappers import internal_error_handler
from src.utils.wrappers import require_authorized

# print current root for debugging
print("Running from {0}".format(os.getcwd()))
# load config file and exit on error
print("Loading configuration file...")
if not ini.init_config('smart_sensors_api.ini'):
    print("Configuration file is missing. Server can't be started !")
    exit(-1)

# set locale
locale.setlocale(locale.LC_ALL, ini.config('APP', 'locale', default='fr_FR.UTF-8'))

# initialize sensors module
sensors.init()

# create our little application :)
app = Flask(__name__)

# check Configuration section for more details
app.config.from_object(__name__)

# load secret key from configuration file or generated a UUID and use it as secret key
app.secret_key = ini.config('APP', 'secret_key', default=str(uuid.uuid4()))

# enable/disable debug
app.debug = ini.config('APP', 'debug', default=False, boolean=True)
if not app.debug:
    print("Debugger is disabled !")
else:
    print("Debugger is enabled.")

# allow cross origin requests on this application
#CORS(app, resources={'/': {'origins': '*'}, '/': {'supports_credentials': True}})

# ------------------------------------------------------------------------------------------
#                               FLASK ROUTES HANDLERS
# ------------------------------------------------------------------------------------------

#@app.before_request
#def beforeRequest():
#    if not app.debug and 'https' not in request.url:
#        return redirect(request.url.replace('http', 'https'))

@app.route('/', methods=['POST'])
@internal_error_handler('R00TK0')
def root():
    """
        This is the main application's route. It displays the application main page.
    """
    content = """
---------------------------------- SMART SENSORS API ----------------------------------
Get information POSTing to /usage with your API secret key
Your post data must always (whatever the route you are querying) contain at least:
{
    'api_key':'<your_secret_api_key_here>'
}
---------------------------------------------------------------------------------------
    """
    return json_response(Response(False, content).json(), status_code=200)

# ---------------------------------------- HELP RELATED ROUTES ----------------------------------------

@app.route('/usage', methods=['POST'])
@internal_error_handler('USAGE')
@require_authorized()
def usage():
    """
        This route is used to display API Manual
    """
    content = """
---------------------------- SMART SENSORS API USER MANUAL ----------------------------
[POST] /report
    api_key: your API secret key

    Get a list of all sensors and a short description for each of them

[POST] /report/subscribe
    api_key: your API secret key
        url: your callback url
    dev_eui: device identifier

    Subscribe to a sensor's data stream to receive data from this sensor periodically

[POST] /report/subscribe
    api_key: your API secret key
        url: your callback url
    dev_eui: device identifier

    Unsubscribe to a sensor's data stream to stop receiving data from this sensor to this url

Data payload example for a POST to /report/subscribe:
{
    'api_key':'<your_secret_api_key_here>',
    'url':'<your_callback_url>', # (ex: http://requestb.in/your_bin_id)
    'dev_eui':'<device_identifier>' # (ex: {0123-4567-89AB-CDEF})
}
---------------------------------------------------------------------------------------
    """
    return json_response(Response(False, content).json(), status_code=200)

# ---------------------------------------- REPORT RELATED ROUTES ----------------------------------------

@app.route('/report', methods=['POST'])
@internal_error_handler('REP')
@require_authorized()
def report():
    """
        This route is used to display a report of registered sensors
    """
    err = True
    code = 200
    content = sensors.report()
    if content is None:
        content = "An error occurred while creating the report. Try again later."
    else:
        err = False
    return json_response(Response(err, content).json(), status_code=code)

@app.route('/report/subscribe', methods=['POST'])
@internal_error_handler('REP_SUB')
@require_authorized()
def report_subscribe():
    """
        This route is used to 
    """
    err = True
    code = 200
    callback = request.form['callback']
    dev_eui = request.form['dev_eui']
    content = "An error occured, callback parameter is not a valid url."
    if validator.validate(callback, 'url'):
        content = "An error occured, dev_eui parameter is not a valid device EUI."
        if validator.validate(dev_eui, 'eui64'):
            content = "An error occured, subscription failed."
            if sensors.subscribe(callback, dev_eui):
                content = "Successfully subscribed, you should be receiving data soon."
                err = False
    return json_response(Response(err, content).json(), status_code=code)

@app.route('/report/unsubscribe', methods=['POST'])
@internal_error_handler('REP_UNSUB')
@require_authorized()
def report_unsubscribe():
    """
        This route is used to
    """
    err = True
    code = 200
    callback = request.form['callback']
    dev_eui = request.form['dev_eui']
    content = "An error occured, callback parameter is not a valid url."
    if validator.validate(callback, 'url'):
        content = "An error occured, dev_eui parameter is not a valid device EUI."
        if validator.validate(dev_eui, 'eui64'):
            content = "An error occured, unsubscription failed."
            if sensors.unsubscribe(callback, dev_eui):
                content = "Successfully unsubscribed, you should stop receiving data from now on."
                err = False
    return json_response(Response(err, content).json(), status_code=code)

# ---------------------------------------- FLASK ERROR HANDLERS ----------------------------------------

@app.errorhandler(404)
def not_found(msg):
    """
        This is an error handler for 404 NOT FOUND exception
    """
    return json_response(Response(True, "Not found").json(), status_code=404)

# ------------------------------------------------------------------------------------------
#                               SERVER RUN FUNCTION
# ------------------------------------------------------------------------------------------

def run():
    """
        Start the application (dev only)
    """
    print("Starting SmartSensors API...")
    app.run(host='0.0.0.0', port=5000)

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

def test():
    """
        Module unit tests
    """
    print('SMART_SENSORS - TESTS NOT IMPLEMENTED')
