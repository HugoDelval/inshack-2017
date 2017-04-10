# WriteUp - Secure Garden Shed v1.0

You need to reverse the `.sgsc` file format.

You can achieve this by reversing the binary `sgs-exec-release`

Indeed, this binary starts by parsing the file format to load (and **decrypt**) 
static data from `.data` section and instructions from `.code` section.

Once you've done that you should be able to notice that there is a simple algorithm (XOR) used 
to decrypt data section and the key is stored, **plaintext**, in the same file.

Then you need to find key offset and data section offset and write an exploit which dumps 
the data section once it is decrypted.

You've got the flag !
