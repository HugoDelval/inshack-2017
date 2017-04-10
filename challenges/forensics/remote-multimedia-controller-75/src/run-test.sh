#!/usr/bin/env bash
# -!- encoding:utf8 -!-
#-----------------------------------------------------------------------
# file:   run-test.sh
# date:   2017-01-16
# author: paul.dautry
# purpose:
#       Execute trusted clients to create bogus traffic used for the 
#       Wireshark capture
#-----------------------------------------------------------------------

#./bin/multimedia-server &> logs/multimedia-server.log &
./bin/client-trusted-1
./bin/client-trusted-2
python3 bin/exploit.py
#./bin/client-trusted-3
