import matplotlib.pyplot as plt
import time

from functions import draw_graph, modified_karger_algorithm, min_cut, plot_graph
from circuits import random_circuit, cut_growth

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

#Example to use the functions
# qc = random_circuit.random_circuit(n_qubits = 10, depth = 30, name = "prueba")
# circuit_image = qc.draw(output='mpl')
# circuit_image.savefig(f'results/prueba2_circuit.png')

# G, pos, qubit_top_nodes, name = draw_graph.circuit_to_graph(qc)

# draw_graph.draw_circuit_graph(G, pos, name = f"{name}_Graph")

# exclude_nodes = [4, 5]

# min_cut_value = min_cut.min_cut(qc, exclude_nodes, trials=30, bool_cuts=True, bool_plot=True)

# If you want to calculate the min_cut one time
# min_cut_value = modified_karger_algorithm.karger_min_cut_circuit(qc, exclude_nodes, bool_plot=False)

# draw_graph.cut_animation("results/graphs/min_cut_prueba", "animation1")



# Example to use the cut_growth functionS

total_qubits = 10
total_depth = 200
exclude_nodes = [0, 1]

start_time = time.time()

cut_growth.cut_growth(total_qubits=total_qubits, total_depth=total_depth, exclude_nodes=exclude_nodes, circuits_trials=20, cut_trials=40)
#cut_growth.cut_growth_exclude(n_qubits=total_qubits, depth=total_depth, circuits_trials=20, cut_trials=40)
end_time = time.time()

# Calcula el tiempo transcurrido
elapsed_time = end_time - start_time

# Imprime el tiempo transcurrido
print(f"El tiempo de ejecución fue de {elapsed_time:.2f} segundos.")

plot_graph.plot_graphs_depth(total_qubits, total_depth, exclude_nodes)
plot_graph.plot_graphs_qubits(total_qubits, total_depth, exclude_nodes)
# plot_graph.plot_graphs_exclude(total_qubits, total_depth)