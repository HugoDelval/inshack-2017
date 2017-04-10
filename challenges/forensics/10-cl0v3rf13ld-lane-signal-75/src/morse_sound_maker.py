#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#----------------------------------------------------------------
# file:    morse_sound_maker.py
# date:    2016-02-05
# author:  paul.dautry
# purpose:
#       This file is used to create an audio file containing a
#       morse signal based on a morse alphabet described in this 
#       file
#----------------------------------------------------------------
#-------------------------------------------------------------------------------
#   DEPENDENCIES
#-------------------------------------------------------------------------------
import os
import sys
from subprocess import call
#-------------------------------------------------------------------------------
#   CONSTANTS
#-------------------------------------------------------------------------------
MORSE_SOUNDS_DIR = 'morse_sounds/'
MORSE_SOUNDS = {
    '_': 'long.ogg',
    '.': 'short.ogg',
    ' ': 'white.ogg'
}
WHITE_SOUND = os.path.join(MORSE_SOUNDS_DIR, MORSE_SOUNDS.get(' '))
MORSE_ALPHABET = {
    'A': '._',
    'B': '_...',
    'C': '_._.',
    'D': '_..',
    'E': '.',
    'F': '.._.',
    'G': '__.',
    'H': '....',
    'I': '..',
    'J': '.___',
    'K': '_._',
    'L': '._..',
    'M': '__',
    'N': '_.',
    'O': '___',
    'P': '.__.',
    'Q': '__._',
    'R': '._.',
    'S': '...',
    'T': '_',
    'U': '.._',
    'V': '..._',
    'W': '.__',
    'X': '_.._',
    'Y': '_.__',
    'Z': '__..',
    '0': '_____',
    '1': '.____',
    '2': '..___',
    '3': '...__',
    '4': '...._',
    '5': '.....',
    '6': '_....',
    '7': '__...',
    '8': '___..',
    '9': '____.',
    '.': '._._._',
    ',': '__..__',
    '?': '..__..',
    "'": ".____.",
    '!': '_._.__',
    '/': '_.._.',
    '(': '_.__.',
    ')': '_.__._',
    '&': '._...',
    ':': '___...',
    ';': '_._._.',
    '=': '_..._',
    '+': '._._.',
    '-': '_...._',
    '_': '..__._',
    '"': '._.._.',
    '$': '..._.._',
    '@': '.__._.',
    ' ': ' '
}
MORSE_SUPPORTED_INPUT = sorted(list(MORSE_ALPHABET.keys()))
FUSION_TOOL = ['sox']
FUSION_TOOL_ARGS = ['--combine', 'concatenate']
#-------------------------------------------------------------------------------
#   FUNCTIONS
#-------------------------------------------------------------------------------
def help():
    """help"""
    print('----------------------- Morse Sound Maker -----------------------')
    print('\ninput alphabet: %s' % MORSE_SUPPORTED_INPUT)
    print('\ntranslation table:')
    for inp, val in MORSE_ALPHABET.items():
        print('"%s" -> %s' % (inp, val))
    print('\nsound files:')
    for sym, fname in MORSE_SOUNDS.items():
        fpath = os.path.join(MORSE_SOUNDS_DIR, fname)
        stats = os.stat(fpath)
        print('%s: %s' % (fname, stats))

def sysexec(prog, args):
    cmd = prog + args
    print('sysexec("%s")' % (' '.join(cmd)))
    call(cmd)

def morse_normalize(text):
    """morse_normalize"""
    unmodified = True
    out = ''
    for c in text.upper():
        if not c in MORSE_SUPPORTED_INPUT:
            unmodified = False
            out += '_'
        out += c
    return (unmodified, out)

def morse_encode(text):
    """morse_encode"""
    ok = True
    morse = ''
    for c in text:
        code = MORSE_ALPHABET.get(c, None)
        if code is None:
            ok = False
            break
        morse += code
        morse += ' '
    return (ok, morse[:-1])

def sound_encode(morse):
    ok = True
    sound = [ WHITE_SOUND ]
    for c in morse:
        s = MORSE_SOUNDS.get(c, None)
        if s is None:
            ok = False
            break
        sound.append(os.path.join(MORSE_SOUNDS_DIR, s))
    sound.append(WHITE_SOUND)
    return (ok, sound)

def create_output(sound, outfile):
    args = []
    args += FUSION_TOOL_ARGS
    args += sound
    args.append(outfile)
    sysexec(FUSION_TOOL, args)
#-------------------------------------------------------------------------------
#   SCRIPT
#-------------------------------------------------------------------------------
content = None
if '-h' in sys.argv:
    help()
    exit(0)

if '-f' in sys.argv:
    fpath = input('Enter complete filepath: ')
    with open(fpath, 'r') as f:
        content = f.read()
        if '{' in content:
            print('warn: converting { to (')
            content = content.replace('{', '(')
        if '}' in content:
            print('warn: converting } to )')
            content = content.replace('}', ')')

if content is None:
    content = input('Enter text to encode: ')

if len(content) < 0:
    print('Input content must not be empty!')
    exit(1)

outfile = input('Enter outfile name: ')
while len(outfile) == 0:
    outfile = input('Enter outfile name (must not be empty): ')

(ok, text) = morse_normalize(content)
print('"%s" -> [morse_normalize] -> "%s"' % (content, text))
if not ok:
    print('morse_normalize failed!')
    exit(1)

(ok, morse) = morse_encode(text)
print('"%s" -> [morse_encode] -> "%s"' % (text, morse))
if not ok:
    print('morse_encode failed!')
    exit(1)

(ok, sound) = sound_encode(morse)
print('"%s" -> [sound_encode] -> "%s"' % (morse, sound))
if not ok:
    print('sound_encode failed!')
    exit(1)

print('creating output file...')
create_output(sound, outfile)
print('done!')
exit(0)
