# Solution

The problem to solve here is a knapsack problem, but identifying this won't get you very far because the problems provided by the server are actually unsolvable.
The knapsack resolution is presented in the other Boulicoin problem where the crypto flaws have been fixed and the problem is solveable.

The server sends a list of items, the capacity of the knapsack and the minimum score to obtain, along with the same values encrypted so the server can check we didn't make up data. We do not have posession of the key or the IV so we can't sign the values ourselves.
The trick is that the server does not check if the three encrypted values returned to it come from the same task.
Now we can attack the system by decoupling values and assembling custom jobs that are easy to do. For example, if we get the two jobs :
`{items:[itemsJob1], minScore:800, capacity:50}`
`{items:[itemsJob2], minScore:1000, capacity:100}`
We can send back the encrypted values taken from any job so the server can decrypt the data as:
`{items:[itemsJob1], minScore:800, capacity:100}`
Which will make the problem very easy to solve, and we get a flag in return !
