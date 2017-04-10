#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#----------------------------------------------------------------
# file:    concat.py
# date:    2016-02-05
# author:  paul.dautry
# purpose:
#       This file is used to concatenate multiple files
#----------------------------------------------------------------

import sys

outfile = input('Enter outfile name: ')
while len(outfile) == 0:
    outfile = input('Enter outfile name: ')

with open(outfile, 'wb') as o:
    for k in range(1, len(sys.argv)):
        arg = sys.argv[k]
        with open(arg, 'rb') as f:
            o.write(f.read())

print('done!')
