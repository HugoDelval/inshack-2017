#-----------------------------------------------------------------------
# file:   Makefile
# date:   2017-01-16
# author: paul.dautry
# purpose:
#       Makefile used to build exploit shellcodes and other binaries
#-----------------------------------------------------------------------

all: build_server build_exploit build_clients update_flag

build_server:
	gcc -fno-stack-protector -z execstack c/multimedia-server.c -o bin/multimedia-server

build_exploit:
	nasm -o bin/exploit-stager.o -f elf64 asm/exploit-stager.asm
	nasm -o bin/exploit.o -f elf64 asm/exploit.asm
	ld -o bin/exploit-stager.elf bin/exploit-stager.o
	ld -o bin/exploit.elf bin/exploit.o
	objdump -d bin/exploit-stager.elf > bin/exploit-stager.hex
	objdump -d bin/exploit.elf > bin/exploit.hex

build_clients:
	gcc -DCLIENT_TRUSTED_1 c/client.c -o bin/client-trusted-1
	gcc -DCLIENT_TRUSTED_2 c/client.c -o bin/client-trusted-2
	gcc -DCLIENT_TRUSTED_3 c/client.c -o bin/client-trusted-3

update_flag:
	python3 update_flag.py

test:
	./run-test.sh
