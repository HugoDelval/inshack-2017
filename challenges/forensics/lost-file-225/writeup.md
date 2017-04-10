#Writeup

We see the process and its pid with "ps faux". To be allowed to install python module we need to create virtualenv. To complete this challenge I use pyrasite, to attach to a running process, and uncompyle6 to convert bytecode to python code.

Once we are attached with pyrasite to the process we can uncompyle x. It's a xor. There is another variable: c.
We decode the base64 of c and use the tool xortool to get the key and unxor.

We have now a second python file. After analyze, we have a xor (x), the key (k)  and the flag (data)
