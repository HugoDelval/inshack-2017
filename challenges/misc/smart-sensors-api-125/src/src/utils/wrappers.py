# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                           IMPORTS
# ------------------------------------------------------------------------------------------

import time
from flask_responses import json_response
from flask import request
from functools import wraps
from src.utils.response import Response
from src.utils import ini

# ------------------------------------------------------------------------------------------
#                                          DECORATOR
# ------------------------------------------------------------------------------------------

def _check_authorized(form):
    config_key = ini.config('USER', 'api_key', default=None)
    if config_key is not None and config_key == form['api_key']:
        return True
    return False

def internal_error_handler(err_code):
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                timestamp = time.strftime('%d%m%H%M%S')
                print('mapif.{0}() at {1} error: details below.'.format(f.__name__, timestamp), e)
                code = '{0}.{1}'.format(err_code, timestamp)
                return json_response(Response(has_error=True, code=code, content='').json(), status_code=500)
        return wrapped_f
    return wrapper


def require_authorized():
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if not _check_authorized(request.form):
                return json_response(Response(True, "You're not connected.").json(), status_code=403)
            else:
                return f(*args, **kwargs)
        return wrapped_f
    return wrapper
