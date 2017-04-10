#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    activation.py
# date:    2017-01-12
# author:  paul dautry
# purpose:
#       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DEBUG = False

def print_dbg(msg):
    if DEBUG:
        print(msg)

class Activator(object):
    CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    """docstring for Activator"""
    def __init__(self):
        super(Activator, self).__init__()
        self.z = 36
        self.checksum = [ 30, 24, 18, 12, 6, 0 ]

    def block(self, b, mod):
        print_dbg('call: block(self, b=<%s>, mod=%d)' % (b, mod))
        if len(b) != 6:
            print_dbg('err: incorrect block length (%d)' % len(b))
            return None
        s = 0
        for k in range(0, len(b)):
            l = b[k]
            if l not in Activator.CHARSET:
                print_dbg('err: input not found in charset (%s)' % l)
                return None
            v = abs(Activator.CHARSET.index(l) - (k+1))
            s += v
            print_dbg('current l is: %s' % l)
            print_dbg('current k is: %d' % k)
            print_dbg('current value is: %d' % v)
            print_dbg('current sum is: %d' % s)
        return s % mod

    def activate(self, s):
        print_dbg('call: activate(self, s=<%s>)' % s)
        blocks = s.split('-')
        blocks_sz = len(blocks)
        if blocks_sz != 6:
            print_dbg('err: incorrect number of blocks (%d)' % blocks_sz)
            return False
        for k in range(0, blocks_sz):
            self.z = self.block(blocks[k], self.z)
            print_dbg('dbg: new z is: %d' % self.z)
            if self.z is None:
                print_dbg('err: block function returned error')
                return False
            if self.z != self.checksum[k]:
                print_dbg('err: incorrect checksum (z=%d tested against checksum[%d]=%d)' % (self.z, k, self.checksum[k]))
                return False
        return True
        