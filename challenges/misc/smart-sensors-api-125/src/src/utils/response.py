#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import json

# ------------------------------------------------------------------------------------------
#                                     RESPONSE CLASS
# ------------------------------------------------------------------------------------------

class Response:
    def __init__(self, has_error = True, content = {}, code=None):
        self.has_error = has_error
        self.content = content
        self.code = code

    def json(self):
        return {'has_error': self.has_error, 'content': self.content, 'code': self.code}

    