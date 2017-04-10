#!/usr/bin/env python3
# -!- encoding:utf8 -!-

import time
import requests

CALLBACK = 'http://requestb.in/17o60sj1'
DEV_EUI = '{653F-853E-498B-BE17}'
API_KEY = 'test'

def query(url, data={}):
    resp = requests.post(url, data=data)
    print(resp.text)
    return resp.text

#query('http://localhost:5000/')
#query('http://localhost:5000/usage', {'api_key':API_KEY})
#query('http://localhost:5000/report', {'api_key':API_KEY})
query('http://localhost:5000/report/subscribe', {'api_key':API_KEY, 'callback':CALLBACK, 'dev_eui':DEV_EUI})
time.sleep(40)
query('http://localhost:5000/report/unsubscribe', {'api_key':API_KEY, 'callback':CALLBACK, 'dev_eui':DEV_EUI})
