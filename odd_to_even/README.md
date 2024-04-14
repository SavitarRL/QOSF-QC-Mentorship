# Task 2 Odd to Even
Design a quantum algorithm that when given numbers of range $[1,n)$ and are odd
convert them into even numbers, and they must stay in the same range so they cannot be less than 1 nor greater than n. $n = 2^k$ where k is the number of qubits you are going
to use. There exist multiple solutions.

Example:
```
B = odd_to_even (n = 31,list= [1,2,2,4,5,6,7,11,17,21,22,23] )
print(B)
One possible output is: [2,2,2,4,4,6,8,10,18,20,22,22]
```

### Classical Method

A very straightforward solution: We loop through the array, and when we get to an element which is less than the target, we add that element into an array. We return that array at the end. 

- Time complexity: $\mathcal{O}(n)$ where $n$ is the length of the array, as we are looping through the array once
- Space complexity: $\mathcal{O}(1)$ since we are editing the array in-place

### Quantum Method 

To be done...

References:

[1] Deutsch, David, and Richard Jozsa. &quot;Rapid solution of problems by quantum
computation.&quot; Proceedings of the Royal Society of London. Series A: Mathematical and
Physical Sciences 439.1907 (1992): 553-558.

[2] Bernstein, Ethan, and Umesh Vazirani. &quot;Quantum complexity theory.&quot; SIAM Journal
on computing 26.5 (1997): 1411-1473.

[3] Grover, Lov K. , &quot;A fast quantum mechanical algorithm for database search&quot;,
Proceedings of the 28th Annual ACM Symposium on the Theory of Computing (1996),
arXiv:quant-ph/9605043