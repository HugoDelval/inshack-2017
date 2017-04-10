#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    sgs_compil.py
# date:    2017-01-05
# author:  paul dautry
# purpose:
#      Code du compilateur de fichiers .sgs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
import json

from sgs_compil_utils.sgs_config import SGSConfig
from sgs_compil_utils.cli_option_parser import CLIOptionsParser
from sgs_compil_utils.sgs_parser import SGSParser
from sgs_compil_utils.sgs_compiler import SGSCompiler
from sgs_compil_utils.sgs_assembler import SGSAssembler

# script if main
if __name__ == '__main__':
    # command line arguments parsing
    cliop = CLIOptionsParser(sys.argv)
    if not cliop.parse():
        SGSConfig.fat(cliop.error)
    if not cliop.has_option('-i'):
        SGSConfig.fat("""usage: sgs-compil [options] -i <input_file>
        options:
            -o <output_file>: specify an ouput file.
            -e: encrypts data section of the sgs binary.""")
    # update config runtime arguments
    SGSConfig.RT_VERBOSE = cliop.has_option('-v')
    SGSConfig.RT_DEBUG = cliop.has_option('-d')
    SGSConfig.RT_ENCRYPT = cliop.has_option('-e')
    # parsing stage
    SGSConfig.inf('parser working...')
    parser = SGSParser(cliop.option_value('-i'), cliop.options)
    if not parser.parse():
        SGSConfig.fat(parser.error)
    SGSConfig.inf('parsing completed.')
    SGSConfig.dbg('------------------------------------------------ options')
    SGSConfig.dbg(json.dumps(parser.prog_struct['options'], sort_keys=True, indent=4), True)
    SGSConfig.dbg('------------------------------------------------ data')
    SGSConfig.dbg(json.dumps(parser.prog_struct['data'], sort_keys=True, indent=4), True)
    # ------------- DBG
    # compilation stage
    SGSConfig.inf('compiler working...')
    compiler = SGSCompiler(cliop.options, parser.prog_struct)
    if not compiler.compile():
        SGSConfig.fat(compiler.error)
    SGSConfig.inf('compilation completed.')
    # ------------- DBG
    SGSConfig.dbg('------------------------------------------------ instructions')
    SGSConfig.dbg(json.dumps(parser.prog_struct['instructions'], sort_keys=True, indent=4), True)
    SGSConfig.dbg('------------------------------------------------ asm')
    SGSConfig.dbg(SGSConfig.format_asm(parser.prog_struct['asm']), True)    
    # ------------- DBG
    # assemble stage
    SGSConfig.inf('assembler working...')
    outfile = cliop.option_value('-o', cliop.option_value('-i')+'c')
    assembler = SGSAssembler(outfile, cliop.options, parser.prog_struct)
    if not assembler.assemble():
        SGSConfig.fat(assembler.error)
    SGSConfig.inf('binary completed.')
    SGSConfig.dbg('------------------------------------------------ hexadecimal dump')
    if SGSConfig.RT_DEBUG:
        os.system('hexdump -C %s' % outfile)
    # success
    exit(0)
