#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import re
import requests
import json
from urllib.parse import urlparse
from src.utils import ini

_VALIDATORS_ = {
    'email': re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
    'alphanum': re.compile('^\w+$'),
    'int': re.compile('^\d+$'),
    'double': re.compile('^\d+(\.\d+)?$'),
    'phone': re.compile('^(\+\d{2}(\s)?\d|\d{2})(\s)?(\d{2}(\s)?){4}$'),
    'year': re.compile('^\d{4}$'),
    'timestamp': re.compile('^\d{4}(-\d{2}){2}$'),
    'eui64': re.compile('\{([0-9A-F]{4}-){3}[0-9A-F]{4}\}')
}

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------

def validate(field, vtype=None):
    """
        (In)Validates data based on its type using regular expressions
    """
    if vtype == 'url':
        url = urlparse(field)
        return url.scheme == 'http'
    elif vtype in _VALIDATORS_.keys():
        return True if _VALIDATORS_[vtype].match(str(field)) else False
    else:
        return False

def is_empty(field):
    """
        Tests if a field is empty
    """
    return len(str(field).strip()) == 0
