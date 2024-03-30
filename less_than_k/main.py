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
