#!/bin/bash
# -!- encoding:utf8 -!-
#-------------------------------------------------------------------------------
# file:    test.sh
# date:    2017-03-05
# author:  paul.dautry
# purpose:
#       This script runs multiple tests
#-------------------------------------------------------------------------------

BIN=${1}
SGS_BIN=${2}

function run_test {
    echo "run_test ${1} compared to ${2}:"
    ${BIN} ${SGS_BIN} 1> tests/ouput 2> logs/sgs-exec.log < ${1}
    val=$(diff -q tests/ouput ${2} |wc -l)
    if [[ ${val} -eq 0 ]]; then
        echo "success!"
    elif [[ ${val} -eq 1 ]]; then
        echo "failed!"    
    fi
}


run_test tests/lock-fail-0.input tests/lock-fail.output
run_test tests/lock-fail-1.input tests/lock-fail.output
run_test tests/lock-fail-2.input tests/lock-fail.output
run_test tests/lock-fail-3.input tests/lock-fail.output
run_test tests/lock-success.input tests/lock-success.output
