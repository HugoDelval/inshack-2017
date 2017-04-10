#!/usr/bin/env bash
# -!- encoding:utf8 -!-
#----------------------------------------------------------------
# file:    build.sh
# date:    2016-02-05
# author:  paul.dautry
# purpose:
#       This file is used to create challenge file
#----------------------------------------------------------------

echo -e "flag.txt\ncapture.ogg" | ./morse_sound_maker.py -f
echo "find_me.png" | ./concat.py 10-Cloverfield-Lane.jpg morse_code.png capture.ogg
