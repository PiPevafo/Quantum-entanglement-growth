from circuits import random_circuit
from functions import min_cut
import multiprocessing
import numpy as np
import os
from functools import partial
import concurrent.futures

# Función que se encargará de calcular el min_cut para un único trial
def calculate_min_cut(n_qubits, depth, trial, exclude_nodes, dat_file_path_circuits):
    name = f"{trial}"
    # Generar circuito aleatorio
    qc = random_circuit.ramdon_circuit(n_qubits=n_qubits, depth=depth, name=name, bol_dat=False, dat_file_path=dat_file_path_circuits)
    # Calcular min_cut
    min_cut_value = min_cut.min_cut(qc, exclude_nodes, 10, False, False)
    return min_cut_value

# Función que se encargará de manejar todos los trials para una combinación específica de n_qubits y depth
def process_trials(n_qubits, depth, exclude_nodes, trials, dat_file_path_circuits):
    min_cut_values = []
    
    # Usar un executor para manejar los trials en paralelo
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Preparar una lista de tareas para los trials
        futures = [executor.submit(calculate_min_cut, n_qubits, depth, trial, exclude_nodes, dat_file_path_circuits) for trial in range(trials)]
        
        # Recoger los resultados a medida que se completan
        for future in concurrent.futures.as_completed(futures):
            min_cut_values.append(future.result())
    
    # Calcular el valor promedio de min_cut
    return np.mean(min_cut_values)

# Función principal
def cut_growth(total_qubits, total_depth, exclude_nodes, trials):
    
    dat_file_path_circuits = f'results/circuits/qubits{total_qubits}_depth{total_depth}/circuits.dat'
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results.dat'
    
    if not os.path.exists(f'results/circuits/qubits{total_qubits}_depth{total_depth}'):
        os.makedirs(f'results/circuits/qubits{total_qubits}_depth{total_depth}')
    
    # Abrir archivo de resultados
    with open(dat_file_path_results, 'w') as dat_file:
        dat_file.write(f'qubits depth min_cut_value\n')
        
        # Iterar sobre cada combinación de n_qubits
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for n_qubits in range(total_qubits, total_qubits + 1):
                # Preparar una lista de tareas para cada profundidad
                futures = {depth: executor.submit(process_trials, n_qubits, depth, exclude_nodes, trials, dat_file_path_circuits) for depth in range(1, total_depth + 1)}
                
                # Recoger los resultados y escribirlos en el archivo
                for depth, future in futures.items():
                    min_cut_value = future.result()
                    dat_file.write(f'{n_qubits} {depth} {min_cut_value}\n')




# Sin paralelizar
# def cut_growth(total_qubits, total_depth, exclude_nodes, trials):
    
#     dat_file_path_circuits = f'results/circuits/qubits{total_qubits}_depth{total_depth}/circuits.dat'
#     dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results.dat'
    
#     if not os.path.exists(f'results/circuits/qubits{total_qubits}_depth{total_depth}'):
#         os.makedirs(f'results/circuits/qubits{total_qubits}_depth{total_depth}')
    
#     with open(dat_file_path_results, 'w') as dat_file:
#         dat_file.write(f'qubits depth min_cut_value\n')
#         with multiprocessing.Pool(processes=24) as pool:
#             for n_qubits in range(3, total_qubits + 1):
#                 for depth in range(1, total_depth + 1):
#                     min_cut_values = []
#                     for trial in range(trials):
#                         name = f"{trial}"
#                         qc = random_circuit.ramdon_circuit(n_qubits=n_qubits, depth=depth, name=name, bol_dat=False, dat_file_path=dat_file_path_circuits)
#                         min_cut_value = min_cut.min_cut(qc, exclude_nodes, trials, False, False)
#                         min_cut_values.append(min_cut_value)

#                     min_cut_value = np.mean(min_cut_values)
#                     # save data
#                     dat_file.write(f'{n_qubits} {depth} {min_cut_value}\n')
                    
                    