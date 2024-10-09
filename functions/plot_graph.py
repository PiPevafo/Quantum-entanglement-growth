import matplotlib.pyplot as plt

#necesito graficar los datos de una lista donde las columnas son qubits depth min_cut_value, y quiero graficar min_cut_value vs depth para cada qubits
def plot_graphs(dat_file_path_results):
    # Leer el archivo de resultados
    with open(dat_file_path_results, 'r') as dat_file:
        dat_file.readline() # Saltar la primera línea
        data = dat_file.readlines()
    
    # Crear un diccionario para almacenar los datos
    results = {}
    
    # Iterar sobre cada línea del archivo
    for line in data:
        qubits, depth, min_cut_value = line.split()
        qubits = int(qubits)
        depth = int(depth)
        min_cut_value = float(min_cut_value)
        
        # Agregar el valor de min_cut al diccionario
        if qubits not in results:
            results[qubits] = {'depth': [], 'min_cut_value': []}
        
        results[qubits]['depth'].append(depth)
        results[qubits]['min_cut_value'].append(min_cut_value)
    
    # Graficar los resultados
    for qubits, values in results.items():
        plt.plot(values['depth'], values['min_cut_value'], label=f'{qubits} qubits')
    
    plt.xlabel('Depth')
    plt.ylabel('Min Cut Value')
    for qubits, values in results.items():
        plt.scatter(values['depth'], values['min_cut_value'])
    plt.legend()
    plt.savefig('results/graphs/min_cut_value_vs_depth.png')
    return results



 