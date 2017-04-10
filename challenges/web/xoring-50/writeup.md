# Solution

The credentials are harcoded. You can see sending data with the form call a function named "x" and compare the returned result with a hardcoded string.
First solution : deobfuscate the code. You can use online deobfuscators or do it by hand.
Second solution : just give a try by putting the hardcoded string in the function itself (with the console of Firefox for example).

Magically, it will give you the solution. Not because it's a miracle, but because the obfuscated function is ... a XOR ! 

Obfuscation : http://www.finalclap.com/faq/471-javascript-obfusquer-code-source
