#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#-----------------------------------------------------------------------
# file:   update_flag.py
# date:   2017-01-16
# author: paul.dautry
# purpose:
#       Automates flag update
#-----------------------------------------------------------------------

import base64

ROUNDS = 5

content = None
with open('../flags/flags.txt', 'rb') as f:
    content = f.read()
print('> reading: %s' % content)

b64 = content
for i in range(0, ROUNDS):
    print('>> before round n°%d: %s' % (i, b64))
    b64 = base64.b64encode(b64)
    print('>> after round n°%d: %s' % (i, b64))

print('> writing: %s' % b64)
with open('bin/flag.txt', 'wb') as f:
    f.write(b64)

print('> done!')
