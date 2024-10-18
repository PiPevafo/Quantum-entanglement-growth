import matplotlib.pyplot as plt
import numpy as np
import math

 # Plot the results of min_cut vs qubits with depth fixed
def plot_graphs_qubits(total_qubits, total_depth, exclude_nodes, alpha=None):
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'
    
    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline()  # Saltar la cabecera
        data = dat_file.readlines()

    results = {}
    has_entropy = alpha is not None

    # Leer las líneas del archivo
    for line in data:
        if has_entropy:
            qubits, depth, min_cut_value, entropy_value = line.split()
            entropy_value = float(entropy_value)  # La cuarta columna si hay entropy_value
        else:
            qubits, depth, min_cut_value = line.split()
        
        qubits = int(qubits)
        depth = int(depth)
        min_cut_value = float(min_cut_value)

        if depth not in results:
            results[depth] = {'qubits': [], 'min_cut_value': [], 'entropy_value': [] if has_entropy else None}

        results[depth]['qubits'].append(qubits)
        results[depth]['min_cut_value'].append(min_cut_value)

        if has_entropy:
            results[depth]['entropy_value'].append(entropy_value)

    # Graficar min_cut_value vs qubits
    for depth, values in results.items():
        plt.plot(values['qubits'], values['min_cut_value'], label=f'{depth} depth - Min Cut')
        if has_entropy:
            plt.plot(values['qubits'], values['entropy_value'], label=f'{depth} depth - Entropy alpha = {alpha}', linestyle='--')
    
    plt.xlabel('Qubits')
    plt.ylabel('Value')
    plt.legend()
    
    # Añadir scatter para puntos discretos
    for depth, values in results.items():
        plt.scatter(values['qubits'], values['min_cut_value'])
        if has_entropy:
            plt.scatter(values['qubits'], values['entropy_value'])
    
    title = f'Min Cut {"and Entropy " if has_entropy else ""}vs Qubits, cutting through {exclude_nodes} qubits'
    plt.title(title)
    
    # Guardar la gráfica
    filename = f'min_cut_vs_qubits_qubits{total_qubits}_depth{total_depth}'
    if has_entropy:
        filename += f'_alpha{alpha}'
    plt.savefig(f'results/graphs/{filename}.png')
    plt.close()

    return results


# Plot the results of min_cut vs depth with qubits fixed
def plot_graphs_depth(total_qubits, total_depth, exclude_nodes, alpha=None):
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'
    
    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline()  # Saltar la cabecera
        data = dat_file.readlines()

    results = {}
    has_entropy = alpha is not None

    # Leer las líneas del archivo
    for line in data:
        if has_entropy:
            qubits, depth, min_cut_value, entropy_value = line.split()
            entropy_value = float(entropy_value)  # La cuarta columna si hay entropy_value
        else:
            qubits, depth, min_cut_value = line.split()
        
        qubits = int(qubits)
        depth = int(depth)
        min_cut_value = float(min_cut_value)

        if qubits not in results:
            results[qubits] = {'depth': [], 'min_cut_value': [], 'entropy_value': [] if has_entropy else None}

        results[qubits]['depth'].append(depth)
        results[qubits]['min_cut_value'].append(min_cut_value)

        if has_entropy:
            results[qubits]['entropy_value'].append(entropy_value)

    # Graficar min_cut_value vs depth
    for qubits, values in results.items():
        plt.plot(values['depth'], values['min_cut_value'], label=f'{qubits} qubits - Min Cut')
        if has_entropy:
            plt.plot(values['depth'], values['entropy_value'], label=f'{qubits} qubits - Entropy alpha = {alpha}', linestyle='--')

    plt.xlabel('Depth')
    plt.ylabel('Value')
    plt.legend()
    
    # Añadir scatter para puntos discretos
    for qubits, values in results.items():
        plt.scatter(values['depth'], values['min_cut_value'])
        if has_entropy:
            plt.scatter(values['depth'], values['entropy_value'])
    
    title = f'Min Cut {"and Entropy " if has_entropy else ""}vs Depth, cutting through {exclude_nodes} qubits'
    plt.title(title)
    
    # Guardar la gráfica
    filename = f'min_cut_vs_depth_qubits{total_qubits}_depth{total_depth}'
    if has_entropy:
        filename += f'_alpha{alpha}'
    plt.savefig(f'results/graphs/{filename}.png')
    plt.close()

    return results


# Plot the results of min_cut vs exclude_nodes with qubits and depth fixed
def plot_graphs_exclude(total_qubits, total_depth):
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_excludes.dat'
    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline()
        data = dat_file.readlines()

    results = {}

    for line in data:
        exclude_node, min_cut_value = line.split()
        exclude_node = int(exclude_node)
        min_cut_value = float(min_cut_value)
 
        if exclude_node not in results:
            results[exclude_node] = {'min_cut_value': []}
        
        results[exclude_node]['min_cut_value'].append(min_cut_value)

    plt.plot(results.keys(), [values['min_cut_value'] for values in results.values()], label=f'{total_qubits} qubits, {total_depth} depth')
    plt.xlabel('Exclude Nodes [i, i+1]')
    plt.ylabel('Min Cut Value')
    plt.scatter(results.keys(), [values['min_cut_value'] for values in results.values()])
    plt.legend()
    plt.title(f'Min Cut vs Exclude Nodes')
    plt.savefig(f'results/graphs/min_cut_vs_exclude_qubits{total_qubits}_depth{total_depth}.png')
    plt.close()
    return results


# Graficar un histograma de los valores de min_cut, son dos columnas min cut y frecuencia
def histogram_min_cut(total_qubits, total_depth, exclude_nodes, circuits_trials):
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/histogram_{exclude_nodes}.dat'
    
    # Leer los datos del archivo
    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline()  # Saltar la primera línea (encabezado)
        data = dat_file.readlines()

    results = {}

    # Procesar los datos
    for line in data:
        min_cut_value, frequency = line.split()
        min_cut_value = float(min_cut_value)
        frequency = int(frequency) / circuits_trials
        results[min_cut_value] = frequency 

    # Graficar el histograma
    plt.bar(results.keys(), results.values(), label='Histogram')

    if total_qubits == 3:
        # Calcular y graficar la función P(x)
        x_values = np.linspace(0, total_depth, 500, endpoint=False)[1:] # Generar 500 puntos entre 0 y total_depth
        y_values = [
            (math.gamma(total_depth+1) / ( (2 ** total_depth) *  math.gamma(x+1) * math.gamma(total_depth-x+1) ))
            for x in x_values
        ]
        
        plt.plot(x_values, y_values, color='red', linestyle='-', label='P(x)')


    # Etiquetas y título
    plt.xlabel('Min Cut Value')
    plt.ylabel('Frequency')
    plt.title(f'Min Cut Value Frequency, cutting through {exclude_nodes} qubits')
    plt.legend()

    # Guardar la gráfica
    plt.savefig(f'results/graphs/histogram_qubits{total_qubits}_depth{total_depth}.png')
    plt.close()
    return results



# Viejas funciones 

#Function to plot the results of min_cut vs depth with qubits fixed
# def plot_graphs_depth(total_qubits, total_depth, exclude_nodes, alpha=None):
    
#     dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'

#     with open(dat_file_path_results, 'r') as dat_file:
#         dat_file.readline() # Saltar la primera línea
#         data = dat_file.readlines()
    

#     results = {}
#     has_entropy = alpha is not None
        
#     for line in data:
#         qubits, depth, min_cut_value = line.split()
#         qubits = int(qubits)
#         depth = int(depth)
#         min_cut_value = float(min_cut_value)

#         if qubits not in results:
#             results[qubits] = {'depth': [], 'min_cut_value': []}
        
#         results[qubits]['depth'].append(depth)
#         results[qubits]['min_cut_value'].append(min_cut_value)

#     for qubits, values in results.items():
#         plt.plot(values['depth'], values['min_cut_value'], label=f'{qubits} qubits')
    
#     plt.xlabel('Depth')
#     plt.ylabel('Min Cut Value')
#     for qubits, values in results.items():
#         plt.scatter(values['depth'], values['min_cut_value'])
#     plt.legend()
#     plt.title(f'Min Cut vs Depth, cutting through {exclude_nodes} qubits')
#     plt.savefig(f'results/graphs/min_cut_vs_depth_qubits{total_qubits}_depth{total_depth}.png')
#     plt.close()
#     return results

# # Plot the results of min_cut vs qubits with depth fixed
# def plot_graphs_qubits(total_qubits, total_depth, exclude_nodes):
#     dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'
#     with open(dat_file_path_results, 'r') as dat_file:
#         dat_file.readline()
#         data = dat_file.readlines()

#     results = {}

#     for line in data:
#         qubits, depth, min_cut_value = line.split()
#         qubits = int(qubits)
#         depth = int(depth)
#         min_cut_value = float(min_cut_value)
 
#         if depth not in results:
#             results[depth] = {'qubits': [], 'min_cut_value': []}
        
#         results[depth]['qubits'].append(qubits)
#         results[depth]['min_cut_value'].append(min_cut_value)

#     for depth, values in results.items():
#         plt.plot(values['qubits'], values['min_cut_value'], label=f'{depth} depth')
    
#     plt.xlabel('Qubits')
#     plt.ylabel('Min Cut Value')
#     for depth, values in results.items():
#         plt.scatter(values['qubits'], values['min_cut_value'])
#     plt.legend()
#     plt.title(f'Min Cut vs Qubits, cutting through {exclude_nodes} qubits')
#     plt.savefig(f'results/graphs/min_cut_vs_qubits_qubits{total_qubits}_depth{total_depth}.png')
#     plt.close()
#     return results