from qiskit import *
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import DensityMatrix
from qiskit_ibm_runtime import QiskitRuntimeService


import matplotlib.pyplot as plt

from functions import draw_graph
from functions import modified_karger_algorithm
from functions import min_cut

 
 
#Create my circuit
n_qubits = 10
n_partition = 4

qc = QuantumCircuit(n_qubits)
qc.name = "prueba"
qc.h(0)
qc.cx(6,7)
qc.cx(7, 8)
for i in range(9):
    qc.cx(i, i+1)

qc.cx(3, 4)
qc.cx(4, 5)
qc.swap(4, 5)

G, pos, qubit_top_nodes, name = draw_graph.circuit_to_graph(qc)

# Show the circuit and graph
circuit_image = qc.draw(output='mpl')
circuit_image.savefig('results/Circuit.png')


draw_graph.draw_circuit_graph(G, pos, name = "Graph")

exclude_nodes = [3, 4]

min_cut.min_cut(qc, exclude_nodes, 1, True, True)

draw_graph.cut_animation("results/graphs/min_cut_prueba", "animation")