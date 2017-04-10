# WriteUp - Secure Garden Shed v2.0

This time you need to find an extra feature added to the binary which can be used using a 
flaw in the SGS-ASM specifications.

If you look closely to these specifications, you'll see that ASM instruction #7 is deprecated.

But did The SGS Company took care of this change in its binary. 

Now you want to trigger the execution of the code instruction #7 to see what happens.


2 ways of doing this :

 + run program in gdb and jump manually inside the function using `set $pc = <#7_asm_instr_handler_addr>`
 + forge a `.sgsc` file with an instruction which calls #7 asm_instr_handler

You've got the flag!
