# Solution

The key is very hard to factor (it has actually more than two factors to generate it faster, there are a lot of 512 bit factors), but it doesn't matter.
RSA's basic math is :
ciphertext = message^exponent mod n
However, as n is very large, the modulus is useless and the ciphertext is only message^exponent. Since we have the ciphertext and the exponent, we only have to compute the 65537th root of c to get m !
