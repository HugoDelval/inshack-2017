#!/usr/bin/env python3
# -!- encoding:utf8 -!-

import time
import requests

def __notify(dev_eui, callback):
    timestamp = time.strftime('on %Y-%m-%d at %H:%M:%S')
    data = {
        'from': dev_eui,
        'timestamp': timestamp,
        'data': None
    }
    if dev_eui == '{653F-853E-498B-BE17}': # FlagRaiserOne
        data['data'] = 'INSA{Dumb_4nd_Dumb3r!Cl34n_G1t_H1st0rY!}' 
    elif dev_eui == '{7446-8FFD-4243-B5F1}': # IntrusionDetectionSensor-Back-Door
        data['data'] =  'Get ready to be robbed in daylight ;)'
    elif dev_eui == '{05BB-C844-479B-812F}': # PersonnalAssistant
        data['data'] = 'Your next appointment is a very personnal matter: go see your psychologist you crazy guy ;)'
    requests.post(callback, data=data, timeout=1)

def notify(subscription_dict):
    timestamp = time.strftime('on %Y-%m-%d at %H:%M:%S')
    print('notify called %s.' % timestamp)
    for dev_eui, callbacks in subscription_dict.items():
        print('\tsending info to callbacks of dev: %s' % dev_eui)
        for callback in callbacks:
            time.sleep(0.3)
            print('\t\tsending to callback %s' % callback)
            __notify(dev_eui, callback)