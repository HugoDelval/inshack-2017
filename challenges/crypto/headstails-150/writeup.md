# Solution

This chllenge uses a very weak hash to verify inputs. It is very easy to generate collisions by switching  bit or two in an input.
Having two strings with the same hash where one string contains `heads` and the other `tails` is not very hard either.
We can launch a birthday attack (more precisely a meet-in-the-middle attack) by generating a lot of strings like `86523520heads` and `685421056tails` and try to find collisions between the two sets.
Otherwise if you're a bit crazy (and smart) I'm sure there is a way to generate collisions or preimages in constant time.
One of the collising pair is `155171heads` / `146262tails` with the hash `00OooooOOOoOooO00ooo0`.
Now, we can send `00OooooOOOoOooO00ooo0` to the server, and reply either `155171heads` or `146262tails` depending on what it asks for. 100 games later, we get the flag !
