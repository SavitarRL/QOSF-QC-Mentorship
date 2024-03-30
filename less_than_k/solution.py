import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from qiskit.primitives import Sampler
from qiskit_algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from typing import Union
from qiskit.visualization import plot_histogram

class ClassicalSolution:
    """Provides a classical solution for finding numbers less than a given value."""

    @staticmethod
    def less_than_k(k: int, list_n: list[int]) -> list[int]:
        """
        Returns numbers in list_n that are less than k.

        Args:
            k (int): The given value.
            list_n (list[int]): List of positive numbers.

        Returns:
            list[int]: List of unordered numbers less than k.
        """
        result = []
        for num in list_n:
            if num < k:
                result.append(num)
        return result

class QuantumSolution:
    """Provides a quantum solution for finding numbers less than a given value."""

    def __init__(self, k, list_n) -> None:
        """
        Initializes QuantumSolution with the given value k and list of numbers list_n.

        Args:
            k (int): The given value.
            list_n (list[int]): List of positive numbers. 
        """
        self.k = k
        self.list_n = list_n
        self.num_qubits_elem = int(np.log2(max(list_n))) + 1
        self.num_qubits_k = int(np.log2(k)) + 1
        self.num_qubits = max(self.num_qubits_elem, self.num_qubits_k)
        self.init_qc = None
        self.grover_operator = None

    def _encode_problem(self) -> Union[np.ndarray, list[str]]:
        """
        Encodes elements of list_n and numbers which are less than k to their binary representations.
        This step is to prepare the information to be encoded in a quantum circuit.

        Returns:
            Union[np.ndarray, list[str]]: 
            initial_state (np.ndarray): Initial state vector to be prepared in the quantum circuit.
            good_states (list[str]): List of binary representations of good states to be marked in Grover's oracle.
        
        Note:
            In this implementation, we are converting numbers to their binary representation in list_n and searching for good states in the same loop.
            If we were to do these separately, runtime complexity would be O(2n), whereas doing it in the same loop will would be O(n).
            This is to improve runtime. 
        """
        initial_state = np.zeros(2**self.num_qubits)
        good_states = []

        for num in self.list_n:
            # Convert the number to a binary string and zero-pad it
            element_reg = '{0:b}'.format(num).zfill(self.num_qubits)
            
            # Set the corresponding element in the initial state vector to 1
            initial_state[int(element_reg, 2)] = 1
            
            if num < self.k:
                # Convert the current number (num) into its binary representation
                # Format the binary representation with zero-padding to ensure a fixed width
                binary_rep = format(num, '0{}b'.format(self.num_qubits))
                good_states.append(binary_rep)
        
        # Normalize the initial state vector
        initial_state /= np.linalg.norm(initial_state)
        
        return initial_state, good_states
    
    def _initial_circuit(self, initial_state: np.ndarray) -> QuantumCircuit:
        """
        Builds the initial quantum circuit with the prepared initial state, encoding information in list_n.

        Args:
            initial_state (np.ndarray): Initial state vector for numbers in list_n.

        Returns:
            QuantumCircuit: Initialized quantum circuit with the initial states.
        """
        qc = QuantumCircuit(self.num_qubits)
        prepare_state = StatePreparation(initial_state)
        qc.append(prepare_state, range(self.num_qubits))
        return qc

    def grover_oracle(self, marked_states: list[str]) -> QuantumCircuit:
        """
        Builds the quantum circuit for the Grover oracle for multiple marked states.

        Args:
            marked_states (list[str]): Marked states of the oracle.

        Returns:
            QuantumCircuit: Quantum circuit representing the Grover oracle.

        Note: 
            Implementation is done with reference to: https://learning.quantum.ibm.com/tutorial/grovers-algorithm
        """
    
        qc = QuantumCircuit(self.num_qubits)

        # Iterate through each marked state
        for target in marked_states:
            # Reverse the target state string
            rev_target = target[::-1]
            # Find indices of '0's in the reversed target state string
            zero_idxs = [idx for idx in range(self.num_qubits) if rev_target.startswith("0", idx)]
            # Apply X gates to flip '0's to '1's
            qc.x(zero_idxs)
            # Apply multi-controlled Z gate
            qc.compose(MCMT(ZGate(), self.num_qubits - 1, 1), inplace=True)
            # Apply X gates again to restore the state
            qc.x(zero_idxs)

        return qc


    
    def less_than_k(self , tolerance = 0.05) -> Union[list[int], dict]:
        """
        Finds numbers less than the given value k using Grover's algorithm.

        Args:
            tolerance (float): Tolerance level for accepting solutions. We accept solutions +/-tolerance. default value is 0.05 
        Returns:
            Union[list[int], dict]: 
            final_result (list[int]): List of numbers less than k.
                                      Due to the circuit results, the list of numbers will be already sorted 
            grover_result (dict): Output information of the Grover oracle of type GroverResult.
        """
        # Encode the problem into an initial state vector and list of good states
        init_state, good_states = self._encode_problem()

        if not good_states:
            # If no good states, return empty list and empty dictionary
            return [], {}

        # Build the initial quantum circuit with the prepared initial state
        init_qc = self._initial_circuit(init_state)
        self.init_qc = init_qc

        # Build the Grover oracle using the list of good states
        oracle = self.grover_oracle(good_states)
        self.grover_operator = GroverOperator(oracle, insert_barriers=True)

        # Define the amplification problem
        problem = AmplificationProblem(oracle, state_preparation=init_qc, is_good_state=good_states)
        # Run Grover's algorithm
        grover_result = Grover(sampler=Sampler()).amplify(problem)

        # Extract the final result within a tolerance interval
        final_result = self.get_results(grover_result = grover_result, tolerance=tolerance)
        
        return final_result, grover_result

    def get_results(self, grover_result: dict, tolerance) -> list[int]:
        """
        The post-processing step to get values which are less than k from Grover's output

        Args:
            result (dict): Output of the Grover oracle of type GroverResult.
            tolerance (float): Tolerance level for accepting solutions. We accept solutions +/-tolerance. 

        Returns:
            list[int]: Sorted list of numbers within the tolerance interval. This is the answer.
        """
        # Get the binary results from Grover's output
        binary_results = grover_result.circuit_results[0]
        
        # Get the probability of the highest measurement outcome
        highest_prob = binary_results[grover_result.top_measurement]
        
        # Convert binary results to decimal
        decimal_results = {int(key, 2): value for key, value in binary_results.items()}
        
        # Define the tolerance interval around the highest probability measurement
        tolerance_interval = (round(highest_prob, 1) - tolerance, round(highest_prob, 1) + tolerance)
        
        # Filter out results within the tolerance interval
        final_result = [num for num, prob in decimal_results.items() if tolerance_interval[0] <= prob <= tolerance_interval[1]]
        
        return final_result

    def plot_answer_histogram(self, grover_result):
        """
        Plots a histogram of quasi-probability against encoded states from list_n.

        Args:
            grover_result: Output of the Grover oracle of type GroverResult.
        
        Returns:
            Image of the histogram of type: matplotlib.Figure
        """
        if grover_result:
            # Convert binary results to decimal
            decimal_results = {int(key, 2): value for key, value in grover_result.circuit_results[0].items()}
            # Plot histogram
            return plot_histogram(decimal_results)
        
    def get_resources(self) -> dict:
        """
        Retrieves the resources used in the quantum solution.

        Returns:
            dict: Resources used, including the number of qubits, as well as the number and types of gates used.
        """
        if self.num_qubits and self.init_qc and self.grover_operator:
            # Decompose the initial quantum circuit and count the operations
            gates_used_init_qc = self.init_qc.decompose(reps=7).count_ops()
            # Decompose the Grover operator and count the operations
            gates_used_grover = self.grover_operator.decompose().count_ops()
            # Combine the operations used in both circuits
            total_gates_used = gates_used_init_qc | gates_used_grover
            # Calculate the total number of gates used
            num_gates_used = sum(gate_counts for gate, gate_counts in total_gates_used.items() if gate != "barrier")
            
            return {"num_qubits": self.num_qubits,
                    "gates_from_state_prep": gates_used_init_qc,
                    "gates_from_oracle": gates_used_grover,
                    "total_gates_used": total_gates_used,
                    "num_gates_used": num_gates_used}


    