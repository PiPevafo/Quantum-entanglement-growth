from qiskit import *
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import DensityMatrix
from qiskit_ibm_runtime import QiskitRuntimeService

import random

# #Create my circuit
# n_qubits = 10
# n_partition = 4

# qc = QuantumCircuit(n_qubits)
# qc.h(0)
# qc.cx(6,7)
# qc.cx(7, 8)
# for i in range(9):
#     qc.cx(i, i+1)

# qc.cx(3, 4)
# qc.cx(4, 5)
# qc.swap(4, 5)


def ramdon_circuit(n_qubits, depth, name, bool_plot = None, bol_dat = None, dat_file_path = None):
    
    qc = QuantumCircuit(n_qubits)
    qc.name = name
    
    if bol_dat is not None and bol_dat == True:
        if dat_file_path is None:
            dat_file_path = f'results/circuits/{n_qubits}_qubits_{depth}_depth/{name}.dat'
        
        with open(dat_file_path, 'a') as dat_file:
            dat_file.write(f'{n_qubits} qubits and {depth} depth\n')
            for i in range(depth):
                qubit = random.randint(0, n_qubits - 2)
                qc.cx(qubit, qubit + 1)
                # Save the qubit pair in the .dat file
                dat_file.write(f'{qubit} {qubit + 1}\n')
            
            dat_file.write('\n')
    else:
        for i in range(depth):
            qubit = random.randint(0, n_qubits - 2)
            qc.cx(qubit, qubit + 1)
            
    if bool_plot is not None and bool_plot == True:
        circuit_image = qc.draw(output='mpl')
        circuit_image.savefig(f'results/{name}_circuit.png')

    return qc