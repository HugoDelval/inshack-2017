#-------------------------------------------------------------------------------
# file: Makefile
# date: 2017-03-05
# author: paul.dautry
# purpose:
#		This file is used to build binaries from sources
#-------------------------------------------------------------------------------
#
# Variables
#
# 	C compiler & other binaries
#
COMP_BIN=gcc
STRIP=strip
#
#	Target Archtecture
#
ARCH=i386
#
# 	C compiler flags
#
bin/sgs-exec-release:COMP_FLAGS=-O3
bin/sgs-exec-release-p:COMP_FLAGS=-O3
bin/sgs-exec-debug:COMP_FLAGS=-Og
ifeq ($(ARCH),i386)
bin/sgs-exec-release:COMP_FLAGS+=-m32 -march=i386
bin/sgs-exec-release-p:COMP_FLAGS+=-m32 -march=i386
bin/sgs-exec-debug:COMP_FLAGS+=-m32 -march=i386
endif
#
#	C compiler defines
#
bin/sgs-exec-debug:COMP_DEFINES+=-DDEBUG
#bin/sgs-exec-debug:COMP_DEFINES+=-DDEBUG_EXEC_STEP_BY_STEP
#bin/sgs-exec-debug:COMP_DEFINES+=-DDEBUG_NO_EXEC
#bin/sgs-exec-debug:COMP_DEFINES+=-DDEBUG_NO_STACK
bin/sgs-exec-release-p:COMP_DEFINES+=-DENABLE_EASTER_EGG
#
#	SGS Compiler flags
#
bin/lock.sgsc:SGS_COMP_FLAGS+=-d
bin/lock.sgsc:SGS_COMP_FLAGS+=-v
bin/lock.sgsc:SGS_COMP_FLAGS+=-e
#
# Rules
#
#	phony rules
#
#.PHONY: build bin/sgs-exec-release bin/sgs-exec-debug bin/lock.sgsc
#
#	all rule: run build rule
#
all: build test
#
#	build rule: builds sgs-exec in both release and debug mode
#
build: bin/sgs-exec-release bin/sgs-exec-release-p bin/sgs-exec-debug bin/lock.sgsc

test: auto-test-release auto-test-release-p
#
#	builds rules for targets
#
bin/sgs-exec-release: tools/sgs-exec
	$(COMP_BIN) $(COMP_FLAGS) $(COMP_DEFINES) $^.c -o $@
	$(STRIP) $@

bin/sgs-exec-release-p: tools/sgs-exec
	$(COMP_BIN) $(COMP_FLAGS) $(COMP_DEFINES) $^.c -o $@
	$(STRIP) $@

bin/sgs-exec-debug: tools/sgs-exec
	$(COMP_BIN) $(COMP_FLAGS) $(COMP_DEFINES) $^.c -o $@
#
#	clean rule
#
clean:
	rm -f bin/*
#
#	auto-test rule: runs tests
#
auto-test-debug:
	./test.sh bin/sgs-exec-debug bin/lock.sgsc

auto-test-release:
	./test.sh bin/sgs-exec-release bin/lock.sgsc

auto-test-release-p:
	./test.sh bin/sgs-exec-release-p bin/lock.sgsc
#
#	generic rules to build targets
#
bin/%.sgsc: tests/%.sgs
	python3 tools/sgs_compil.py $(SGS_COMP_FLAGS) -i $^ -o $@ 1> logs/sgs_compil.log
	hexdump -C $@
