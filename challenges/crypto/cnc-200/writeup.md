AES CBC is used in this challenge to encrypt the session data. The goal is to alter the encrypted cookie to have "is_cnc" set to True.

It is possible because ECB encrypt each block individually and without any checksum on the encrypted data an attacker can reorder the blocks in any order that he wants (as long as the decrypted JSON is still valid).

Here is an example of such an exploit (cf *exploit/exploit.py* for full exploit):

Ask the server to register an user like this one:

```
model = "AAAAtrue],          AAAAA"
localisation = "AAAAAAAAAAAAAAAAA"
password = "AAAAAAAAAAAAAAAAAAA"
bw = 222222222222222
login = "AAAAAAAAAAAAAAAAA"
```

The blocks will be:

```
[["model", "AAAA    0
true],              1
AAAAA"], ["local    2
isation", "AAAAA    3
AAAAAAAAAAAA"],     4
["password", "AA    5
AAAAAAAAAAAAAAAA    6
A"], ["is_cnc",     7
false], ["bw", 2    8
2222222222222],     9
["login", "AAAAA    10
AAAAAAAAAAAA"]]     11
```

And then you can reorder the blocks this way:

```
[["model", "AAAA    0
AAAAA"], ["local    2
isation", "AAAAA    3
AAAAAAAAAAAA"],     4
["password", "AA    5
AAAAAAAAAAAAAAAA    6
A"], ["is_cnc",     7
true],              1
["login", "AAAAA    10
AAAAAAAAAAAA"]]     11
```

Which gives you this session:

```json
[["model", "AAAAAAAAA"], ["localisation", "AAAAAAAAAAAAAAAAA"], ["password", "AAAAAAAAAAAAAAAAAAA"], ["is_cnc", true],          ["login", "AAAAAAAAAAAAAAAAA"]] 
```