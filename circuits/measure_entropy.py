from qiskit import *
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.quantum_info import DensityMatrix
from qiskit.quantum_info import partial_trace
from qiskit.quantum_info import entropy
import numpy as np

# # Define to qubits to observe
# def observed_qubits(n, n_qubits):
#     if n >= n_qubits:
#         raise ValueError("The number of observed qubits must be less than the total number of qubits")
#     observed_qubits = [i for i in range(n)]
    
#     return observed_qubits

# # Reduce density matrix 
# def calculate_reduced_density_matrix(qc, n_partition, n_qubits):
#     # Simulate the circuit
#     simulator = Aer.get_backend('statevector_simulator')
#     circ = transpile(qc, simulator)
#     job = simulator.run(circ)
#     result = job.result()

#     state = result.get_statevector()
    
#     #  Calculate the reduced density matrix
#     reduced_density_matrix = partial_trace(state, [i for i in range(n_qubits) if i not in observed_qubits(n_partition, n_qubits)])
    
#     return reduced_density_matrix

# # Calculate the Von Neumann entropy
# def von_neumann_entropy(qc, n_partition, n_qubits):
#     reduced_density_matrix = calculate_reduced_density_matrix(qc, n_partition, n_qubits)
#     entropy_value = entropy(reduced_density_matrix, base=2)
    
#     return entropy_value

# # Calculate the Hartley entropy
# def hartley_entropy(qc, n_partition, n_qubits):
#     reduced_density_matrix = calculate_reduced_density_matrix(qc, n_partition, n_qubits)
    
#     eigenvalues = np.linalg.eigvals(reduced_density_matrix.data)
#     no_null_eigenvalues = np.count_nonzero(eigenvalues)
#     entropy_value = np.log2(no_null_eigenvalues)
#     return entropy_value

# #Calculate the Rényi entropy
# def renyi_entropy(qc, n_partition, n_qubits, alpha):
#     reduced_density_matrix = calculate_reduced_density_matrix(qc, n_partition, n_qubits)
     
#     # Obtain the eigenvalues of the reduced density matrix
#     rho = DensityMatrix(reduced_density_matrix).data

#     entropy_value = np.log2(np.trace(np.linalg.matrix_power(rho, alpha)))/(1-alpha)   
    
#     return entropy_value.real

# def measure_entropy(qc, n_partition, n_qubits, alpha):
#     if alpha == 0:
#         return von_neumann_entropy(qc, n_partition, n_qubits)
#     if alpha == 1:
#         return hartley_entropy(qc, n_partition, n_qubits)
#     if alpha > 1:
#         return renyi_entropy(qc, n_partition, n_qubits, alpha)
    


# Funciones para las entropías
def von_neumann_entropy(qc, n_partition, n_qubits):
    # Ejecuta el circuito y obtiene el estado final
    state = execute_circuit(qc, n_qubits)
    
    # Traza parcial sobre la partición dada
    reduced_density_matrix = partial_trace(state, range(n_partition, n_qubits))
    
    # Calcula la entropía de von Neumann
    return entropy(reduced_density_matrix, base=2)

def hartley_entropy(qc, n_partition, n_qubits):
    state = execute_circuit(qc, n_qubits)
    reduced_density_matrix = partial_trace(state, range(n_partition, n_qubits))
    eigenvalues = np.linalg.eigvals(reduced_density_matrix.data)
    # eigenvalues = eigenvalues[eigenvalues > 0]  # Descartar valores cero o negativos
    no_null_eigenvalues = np.count_nonzero(eigenvalues)
    entropy_value = np.log2(no_null_eigenvalues)
    
    return entropy_value

def renyi_entropy(qc, n_partition, n_qubits, alpha):
    # Ejecuta el circuito y obtiene el estado final
    state = execute_circuit(qc, n_qubits)
    
    # Traza parcial sobre la partición dada
    reduced_density_matrix = partial_trace(state, range(n_partition, n_qubits))
    
    # Calcula la entropía de Rényi
    eigenvalues = np.linalg.eigvalsh(reduced_density_matrix.data)
    # eigenvalues = eigenvalues[eigenvalues > 0]  # Descartar valores cero o negativos
    renyi = (1 / (1 - alpha)) * np.log2(np.sum(eigenvalues ** alpha))
    
    return abs(renyi)

def execute_circuit(qc, n_qubits):
    # Simulador para obtener el estado final
    simulator = Aer.get_backend('statevector_simulator')
    circ = transpile(qc, simulator)
    job = simulator.run(circ)
    result = job.result()
    
    state = result.get_statevector()
    return state

# Función principal que selecciona el cálculo de entropía
def measure_entropy(qc, n_partition, n_qubits, alpha):
    if alpha == 0:
        return hartley_entropy(qc, n_partition, n_qubits)
    if alpha == 1:
        return von_neumann_entropy(qc, n_partition, n_qubits) 
    if alpha > 1:
        return renyi_entropy(qc, n_partition, n_qubits, alpha) 



#Example
# import random
# n_qubits = 15
# qc = QuantumCircuit(n_qubits)
# for i in range(10):
#     qc.h(i)
# for i in range(22):
#     qc.h(random.randint(0, n_qubits-1))
#     qubit = random.randint(0, n_qubits-2)
#     qc.h(q)
#     qc.cx(qubit, qubit+1)
    
# print(measure_entropy(qc, 4, n_qubits, 0))
# print(measure_entropy(qc, 4, n_qubits, 1))
# print(measure_entropy(qc, 4, n_qubits, 2))
# print(measure_entropy(qc, 4, n_qubits, 3))
# print(measure_entropy(qc, 4, n_qubits, 4))