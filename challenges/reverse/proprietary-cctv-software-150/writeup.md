# WriteUp - Proprietary CCTV Software

Decompile using pycdc/pycdas: 
    
You need to change pycdc code for magic number check not to fail...

For Python 3.5.2+ pyc_module.cpp and pyc_module.h 
magic number is: `0x0A0D0D17` and not `0x0A0D0D16`

pycdc/pycdas is available on Github : [pycdc](https://github.com/zrax/pycdc)  

Reverse key check process and keygen the activator or find out how to decrypt the flag

You should found that the algorithm sums for each block of six characters the indexes of these caracters less (index in bloc plus one)

CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

example:

if block n°1 is '012345' then computation is the following :

* '5' index 0 in block, index in charset `5 => 5 - (0+1) = 4`
* '4' index 1 in block, index in charset `4 => 4 - (1+1) = 2`
* '3' index 2 in block, index in charset `3 => 3 - (2+1) = 0̀`
* '2' index 3 in block, index in charset `2 => 2 - (3+1) = -2`
* '1' index 4 in block, index in charset `1 => 1 - (4+1) = -4`
* '0' index 5 in block, index in charset `0 => 0 - (5+1) = -6̀`

Sum all these to get `4 + 2 + 0 + -2 + -4 + -6 = -6`

Then block 1 sum must validate: 

`sum % 36 == 30` (which is not the case in the example given above)

next block: 

`sum % 30 == 24`
                  
etc.

Do the same thing for all six blocks with the six "targets" to match being : `[ 30, 24, 18, 12, 6, 0 ]`

The following key works :

`V23456-P23456-J23456-D23456-723456-123456`

See exploit/exploit.py for a keygen.

