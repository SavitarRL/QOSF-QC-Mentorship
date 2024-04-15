# Less than k
## Question prompt:
Given a positive integer “k” and a list of integer numbers, look for the numbers within the
list, that are less than k. Consider an appropriate number of qubits and explain why your
proposal is valid for all kinds of numbers in case
Example:
```
A = less_than_k (7,[4,9,11,14,1,13,6,15])
print(A)
[4,1,6]
```

```
├── demo.ipynb          # Jupyter Notebook containing a demonstration of the Quantum Solution implementation.
├── main.py             # Python file containing the main() function for demonstration
├── README.md           # this README file
├── requirements.txt    # Text file listing the dependencies required for the project
├── solution.py         # Python file containing the implementation of the classical and quantum solution
└── tests.py            # Python file containing unit tests for the Quantum Solution implementation.
```
 
## Environment
The current Python version is: `3.12.2`. The project is run in `Microsoft Windows 11 Home`.


## Packages
- **numpy:** 1.26.4
- **qiskit:** 1.0.2
- **qiskit_algorithms:** 0.3.0


## Installation
To install and use this project, follow these steps:


1. **Clone the repository:**
   
   Clone the repository to your local machine using Git. You can do this by running the following command in your terminal or command prompt:


   ```sh
   git clone https://github.com/SavitarRL/QOSF-QC-Mentorship.git
   ```
2. **Navigate to this project directory:**


    Navigate to the root of this project directory
    ```sh
    cd less_than_k
    ```
3.  **Install dependencies**
    Install the required Python packages specified in the `requirements.txt` file
    ```sh
    pip install -r requirements.txt
    ```


## Usage
### To run on terminal
1. Make sure you have Python and the required packages installed on your system.


2. Go to `main.py` in the project directory. The example code is given:
    ```python
    from solution import ClassicalSolution, QuantumSolution
    
    def main():
        k = 7
        list_n = [4,9,11,14,1,13,6,15]
       
        classical_result = ClassicalSolution.less_than_k(k = k, list_n = list_n)

        quantum_solver = QuantumSolution(k = k, list_n = list_n)
        quantum_result, grover_result = quantum_solver.less_than_k()
       
        print("Classical result", classical_result)
        print("Quantum result", quantum_result)
    
    if __name__ == "__main__":
        main()
    ```
3. Save the `main.py` file and run the following in your terminal:
    ```sh
    python main.py
    ```
4. Example output:
    ```
    Classical result [4, 1, 6]
    Quantum result [1, 4, 6]
    ```
You may edit the file as you wish.
### Jupyter Notebook
Open `demo.ipynb` and execute cells within the file. Images of histograms, and quantum circuits for the problem have been added, as well as extra functionalities.


### Running tests
Unit tests are included in the `tests.py` file. To run all tests, run this command in your terminal:
```
python -m unittest discover
```
OR
```
python tests.py
```
## Method
### Classical Method


A very straightforward solution: We loop through the array, and when we get to an element which is less than the target, we add that element into an array. We return that array at the end.


- Time complexity: $\mathcal{O}(n)$ where $n$ is the length of the array, as we are looping through the array once
- Space complexity: $\mathcal{O}(n)$ since the worst case is that all elements in the array are less than the target


### Quantum Method


There exists a quantum algorithm which allows us to search for elements in an unordered or ordered list. Classically, searching through an unordered list takes $\mathcal{O}(n)$ using linear search, and searching through an ordered list takes $\mathcal{O}(\log_2{n})$ using binary search. A quantum solution to searching is using Grover's algorithm [3]. The algorithm will allow us to find the desired elements in a list of length $n$ with $m$ marked elements in \mathcal{O}(\sqrt{n/m})$ time, providing a quadratic speedup.


The technical details, theory and properties of Grover's algorithm can be found here:
- https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/grovers-algorithm
- https://learn.microsoft.com/en-us/azure/quantum/concepts-grovers
- Nielsen, M. A., & Chuang, I. L. (2010). Quantum search algorithms. In Quantum Computation and Quantum Information: 10th Anniversary Edition (pp. 248–276). chapter, Cambridge: Cambridge University Press.


## Implementation
All code for the implementation is in `solution.py`. The classical method is in class `ClassicalSolution`, and the quantum method is in class `QuantumSolution`.


### Computation using Qiskit
#### 1. Encoding the problem
##### State preparation
Using basis encoding, we represent the array of discrete integers to an equal superposition of quantum states. We first convert each number to its binary representation, then represent these as quantum states with equal superposition. E.g. for list_n = [8, 9, 11, 14, 1, 13, 12, 15], the resulting quantum state will be:
$\frac{1}{\sqrt{8}} (|1000\rangle + |1001\rangle + |1011\rangle + |1110\rangle + |0001\rangle + |1101\rangle + |1100\rangle + |1111\rangle)$.
 The `_initial_circuit()` function prepares such state in a quantum circuit.
##### Marking good states
In the same iteration, we convert the elements which are less than $k$ in list_n and convert them into their binary representation. The good states are parsed into the Grover oracle later on. E.g. for list_n = [8, 9, 11, 14, 1, 13, 12, 15] and k = 10, we mark the integers 1, 8, 9, converting them to binary gives:  `['0001', '1000', '1001']`


The conversion to the binary representation of both list_n and marked states is done in the `_encode_problem()` function.
#### 2. Encoding the Grover Oracle
Parsing in the good states found in the `_encode_problem()` function, the `grover_oracle()` method constructs the Grover oracle, marking multiple elements which are less than k.


#### 3. Grover's search/ Amplitude amplification
Used in the `less_than_k` method in the `QuantumSolution` class, we use methods from `AmplificationProblem` and `Grover` from the `qiskit_algorithms` library to run Grover's algorithm and amplify the probabilities of states which are less than k.


#### 4. Measurement and Post-processing
We measure the probabilities of all the states, then we choose the states with the highest amplitudes. From the output of the Grover oracle of type `GroverResult`, the `get_results()` function decodes the results back to decimal numbers. The filtered list of numbers less than k is then obtained by applying a tolerance interval around the highest probability measurement outcome.




### Resources and Runtimes
- Number of qubits:  $N_\text{qubits} = \max{\{ \lceil \log_2({\max{(list\_n)})} \rceil, \lceil \log_2{k} \rceil \}}$. Note that our implementation requires the same number of qubits throughout, therefore we calculate how many qubits we need to encode the numbers in list_n (left) and the number of qubits required to mark the good state (right), then take whatever is larger.
- Runtime complexity for encoding & decoding: We are looping through list_n while encoding the data to $N_\text{qubits}$ number of qubits, while marking $m$
number of good states. In total, using basis encoding to map the problem to qubits takes $\mathcal{O}(n\log_2{N_\text{qubits}})$
- Overall space complexity: We are taking list_n with $\mathcal{O}(n)$ space and encoding it to $n$ number of states, each with $N_\text{qubits}$. As we are creating an equal superposition of $n$ number of states, we only require $N_\text{qubits}$ of qubits. However classically, the worst case is that all elements in the array are less than the target, we still need $\mathcal{O}(n)$ space, which is the same as the classical case.
- Runtime complexity during search: $\mathcal{O}(\sqrt{\frac{n}{m}})$, hence the quadratic speedup. This is the optimised part of the problem.
- Optimal iterations to achieve maximum success probability: $t_{\text{opt}} \approx \frac{\pi}{4} \sqrt{\frac{n}{m}}$
- Probabilities of success: $P(success) = \sin^2\left[ (2t + 1) \arccos\left( \sqrt{\frac{n - m}{m}}\right)\right ]$


### Tests considered and validity
All tests are in `tests.py`. The test cases provided cover various scenarios to ensure the correctness and robustness of the `QuantumSolution` class:


1. All Elements Less Than k: Test cases where all elements in the list are less than the threshold value k.
2. No Elements Less Than k: Cases where none of the elements are less than k.
3. k as Minimum or Maximum Element: Test cases where k is the minimum or maximum element in the list.
4. Some Elements Less Than k: Scenarios where only some elements are less than k.
5. Short and Long Arrays: Test cases with short and long arrays to assess performance across different input sizes.


By testing these scenarios, we verify that our implementation handles different input conditions correctly.


### Improvements and extensions
#### 1. Failure to account for shorter input lists


It is important to acknowledge that during experimentation, our implementation failed for cases where the length of the input list, list_n, is 2. This scenario wasn't covered by our initial set of test cases and highlights a potential edge case that our implementation doesn't handle correctly. This is highly related to the underlying assumption that the Grover algorithm will work when $ m << n$. From this, if there is only $m=1$ marked element against a large array of $n$ elements in list_n, searching will be more viable and reliable.


#### 2. The encoding problem
Our current implementation uses a straightforward encoding method to represent numbers in binary format for quantum state preparation. While our implementation offers a quadratic speedup only in the quantum searching stage, we still need to traverse through list_n in other parts of the code. The encoding runtime takes $\mathcal{O}(n\log_2{N_\text{qubits}})$ and is the limiting factor/bottleneck for overall performance. Exploring more efficient encoding techniques could enhance the overall performance of the algorithm, potentially reducing the number of qubits required and improving the algorithm's scalability.


#### 3. Additional cases to consider -> The encoding problem continued
The cases below heavily relate to the encoding problem discussed previously. This problem is highly significant as it is a crucial step to encode classical information to quantum computers for various applications, such as quantum Machine Learning. A quick overview of different encoding methods can be found in [4].
1. Handling Negative Numbers:


    Our current implementation only considers non-negative integers. Extending the algorithm to handle negative numbers would broaden its applicability to various problems. One approach might be to add a sign bit to the last digit of the binary representation (i.e. `0` for +l `1` for -1. Another), which is known as the two's-complement binary representation [5].


2. Handling Repeating Elements:
    Our current implementation does not capture the case when there are duplicates in list_n. One approach is to preprocess the input list to identify and ignore repeating elements, reducing the problem back to non-repeating elements. Another approach may be to modify the construction of the Grover's oracle to account for repeating elements.


3. Supporting more complex data types:
    The approach we have only accounts for positive integer numbers larger than 0. Extending the implementation to handle floats or imaginary numbers may require more sophisticated encoding techniques. For floats, one may consider these references [6,7] for possible approaches. Complex numbers may be encoded in additional qubits representing the binary representation of the complex part. Practically, complex numbers typically relate to impedance, amplification or dissipation of waves. Incorporating complex numbers in quantum algorithms can be used in solving wave equations (e.g. Helmholtz equation, heat equation etc).


#### 4. Real quantum computers, error mitigation techniques and benchmarking
It is crucial to acknowledge that the algorithm is executed under ideal conditions, simulated by a classical computer. Quantum algorithms, when executed on real quantum hardware, are subject to noise, decoherence, and other imperfections which destroy and alter quantum information. Therefore, error mitigation techniques should be applied and many more experiments should be run to further validate the implementation's performance. The benchmark used for testing and evaluating the algorithm's performance should also be chosen accordingly.


References:


[1] Deutsch, David, and Richard Jozsa. &quot; Rapid solution of problems by quantum
computation.&quot; Proceedings of the Royal Society of London. Series A: Mathematical and Physical Sciences 439.1907 (1992): 553-558.


[2] Bernstein, Ethan, and Umesh Vazirani. &quot; Quantum complexity theory.&quot; SIAM Journal
on computing 26.5 (1997): 1411-1473.


[3] Grover, Lov K. , &quot;A fast quantum mechanical algorithm for database search&quot;,
Proceedings of the 28th Annual ACM Symposium on the Theory of Computing (1996), arXiv:quant-ph/9605043


[4] Weigold, M., Barzen, J., Leymann, F., & Salm, M. (2021). Encoding patterns for quantum algorithms. IET Quantum Communication, 2(4), 141-152. https://doi.org/10.1049/qtc2.12032


[5] Finley, T. (2000, April). Two's Complement. Retrieved from https://www.cs.cornell.edu/~tomf/notes/cps104/twoscomp.html


[6] Wiebe, N., & Kliuchnikov, V. (2013). Floating Point Representations in Quantum Circuit Synthesis. ArXiv. https://doi.org/10.1088/1367-2630/15/9/093041


[7] Seidel, R., Tcholtchev, N., Bock, S., Becker, C. K., & Hauswirth, M. (2021). Efficient Floating Point Arithmetic for Quantum Computers. ArXiv. /abs/2112.10537

