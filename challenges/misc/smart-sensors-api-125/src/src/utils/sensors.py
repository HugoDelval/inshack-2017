#!/usr/bin/env python3
# -!- encoding:utf8 -!-

import time
import json
import _thread
from src.utils.notify import notify

SENSORS = {}
SUBSCRIPTION_DICT = {}

def trigger_notif():
    while True:
        # sleep for some seconds
        time.sleep(30) 
        # force notification
        try:
            notify(SUBSCRIPTION_DICT)
        except Exception as e:
            print(e)
    
def init():
    global SENSORS
    global SUBSCRIPTION_DICT
    # initialize sensors collection
    with open('sensors.json', 'r') as f:
        SENSORS = json.load(f)
    # initialize subscription table
    for s_eui, s_info in SENSORS.items():
        SUBSCRIPTION_DICT[s_eui] = []
    args = ()
    _thread.start_new_thread(trigger_notif,args) #Call itself on a new thread.

def report():
    r = ''
    for s, inf in SENSORS.items():
        r += """----------------------------------------------------------------
device %s:
           name: %s
         vendor: %s
    description: %s
      ds_format: %s
        ds_rate: %s (in seconds)
----------------------------------------------------------------\n""" % (s, 
inf['name'], inf['vendor'], inf['description'], inf['ds_format'], inf['ds_rate'])
    return r

# subscribe vuln: DoS is possible here from an authenticated user, find a way to patch... or not.
def subscribe(callback_url, dev_eui):
    l = SUBSCRIPTION_DICT.get(dev_eui, None)
    if l is not None:
        if not callback_url in l:
            if len(l) > 60:
                l = l[1:]
            l.append(callback_url)
            SUBSCRIPTION_DICT[dev_eui] = l
            return True
    return False
    
def unsubscribe(callback_url, dev_eui):
    l = SUBSCRIPTION_DICT.get(dev_eui, None)
    if l is not None:
        if callback_url in l:
            l.remove(callback_url)
            SUBSCRIPTION_DICT[dev_eui] = l
            return True
    return False