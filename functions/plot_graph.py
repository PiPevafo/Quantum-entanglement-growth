import matplotlib.pyplot as plt

# Function to plot the results of min_cut vs depth with qubits fixed
def plot_graphs_depth(total_qubits, total_depth, exclude_nodes):
    
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'

    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline() # Saltar la primera línea
        data = dat_file.readlines()
    

    results = {}

    for line in data:
        qubits, depth, min_cut_value = line.split()
        qubits = int(qubits)
        depth = int(depth)
        min_cut_value = float(min_cut_value)

        if qubits not in results:
            results[qubits] = {'depth': [], 'min_cut_value': []}
        
        results[qubits]['depth'].append(depth)
        results[qubits]['min_cut_value'].append(min_cut_value)

    for qubits, values in results.items():
        plt.plot(values['depth'], values['min_cut_value'], label=f'{qubits} qubits')
    
    plt.xlabel('Depth')
    plt.ylabel('Min Cut Value')
    for qubits, values in results.items():
        plt.scatter(values['depth'], values['min_cut_value'])
    plt.legend()
    plt.title(f'Min Cut vs Depth, cutting through {exclude_nodes} qubits')
    plt.savefig(f'results/graphs/min_cut_vs_depth_qubits{total_qubits}_depth{total_depth}.png')
    plt.close()
    return results

# Plot the results of min_cut vs qubits with depth fixed
def plot_graphs_qubits(total_qubits, total_depth, exclude_nodes):
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'
    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline()
        data = dat_file.readlines()

    results = {}

    for line in data:
        qubits, depth, min_cut_value = line.split()
        qubits = int(qubits)
        depth = int(depth)
        min_cut_value = float(min_cut_value)
 
        if depth not in results:
            results[depth] = {'qubits': [], 'min_cut_value': []}
        
        results[depth]['qubits'].append(qubits)
        results[depth]['min_cut_value'].append(min_cut_value)

    for depth, values in results.items():
        plt.plot(values['qubits'], values['min_cut_value'], label=f'{depth} depth')
    
    plt.xlabel('Qubits')
    plt.ylabel('Min Cut Value')
    for depth, values in results.items():
        plt.scatter(values['qubits'], values['min_cut_value'])
    plt.legend()
    plt.title(f'Min Cut vs Qubits, cutting through {exclude_nodes} qubits')
    plt.savefig(f'results/graphs/min_cut_vs_qubits_qubits{total_qubits}_depth{total_depth}.png')
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

 