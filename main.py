import matplotlib.pyplot as plt
import time

from functions import draw_graph, modified_karger_algorithm, min_cut, plot_graph
from circuits import random_circuit, cut_growth

 

# qc = random_circuit.ramdon_circuit(n_qubits = 10, depth = 1000, name = "prueba")

# G, pos, qubit_top_nodes, name = draw_graph.circuit_to_graph(qc)

# draw_graph.draw_circuit_graph(G, pos, name = f"{name}_Graph")

# exclude_nodes = [4, 5]

# min_cut.min_cut(qc, exclude_nodes, 100, False, False)

# draw_graph.cut_animation("results/graphs/min_cut_prueba", "animation")

start_time = time.time()

cut_growth.cut_growth(total_qubits=100, total_depth=1000, exclude_nodes=[49,50], trials=20)

end_time = time.time()

# Calcula el tiempo transcurrido
elapsed_time = end_time - start_time

# Imprime el tiempo transcurrido
print(f"El tiempo de ejecución fue de {elapsed_time:.2f} segundos.")

plot_graph.plot_graphs('results/circuits/qubits100_depth1000/results.dat')