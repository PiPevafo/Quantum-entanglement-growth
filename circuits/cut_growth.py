from circuits import random_circuit
from functions import min_cut
import multiprocessing
import numpy as np
import os
import concurrent.futures
from numba import jit

# Function that will be responsible for calculating the min_cut for a single trial

def calculate_min_cut(n_qubits, depth, circuits_trial, exclude_nodes, cut_trials, dat_file_path_circuits):
    name = f"{circuits_trial}"
    # Generar circuito aleatorio
    qc = random_circuit.random_circuit(n_qubits=n_qubits, depth=depth, name=name, bol_dat=False, dat_file_path=dat_file_path_circuits)
    # Calcular min_cut
    min_cut_value = min_cut.min_cut(qc, exclude_nodes, cut_trials, False, False)
    return min_cut_value

# Function that will be responsible for handling all trials for a specific combination of n_qubits and depth

def process_trials(n_qubits, depth, exclude_nodes, circuits_trials, cut_trials, dat_file_path_circuits):
    min_cut_values = []
    
    # Use an executor to handle trials in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
        # Prepare a task list for trials
        futures = [executor.submit(calculate_min_cut, n_qubits, depth, trial, exclude_nodes, cut_trials, dat_file_path_circuits) for trial in range(circuits_trials)]
        
        # Collect results as they are completed
        for future in concurrent.futures.as_completed(futures):
            min_cut_values.append(future.result())
    
    # Calculate the average value of min_cut
    return np.mean(min_cut_values)

# Main function

def cut_growth(total_qubits, total_depth, exclude_nodes, circuits_trials, cut_trials, fixed=None):
    
    dat_file_path_circuits = f'results/circuits/qubits{total_qubits}_depth{total_depth}/circuits.dat'
    dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results_{exclude_nodes}.dat'
    
    if fixed is not None and fixed == 'qubits':
        initial_qubit = total_qubits
    else:  
        initial_qubit = 3
        
    if fixed is not None and fixed == 'depth':
        initial_depth = total_depth
    else:  
        initial_depth = 1
    
    if not os.path.exists(f'results/circuits/qubits{total_qubits}_depth{total_depth}'):
        os.makedirs(f'results/circuits/qubits{total_qubits}_depth{total_depth}')
    
    # Open results file
    with open(dat_file_path_results, 'w') as dat_file:
        dat_file.write(f'qubits depth min_cut_value\n')
        
        # Iterate over each combination of n_qubits
        with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
                for n_qubits in range(initial_qubit, total_qubits + 1):
                    # Prepare a task list for each depth
                    futures = {depth: executor.submit(process_trials, n_qubits, depth, exclude_nodes, circuits_trials, cut_trials, dat_file_path_circuits) for depth in range(initial_depth, total_depth + 1)}
                    
                    # Collect the results and write them to the file
                    for depth, future in futures.items():
                        min_cut_value = future.result()
                        dat_file.write(f'{n_qubits} {depth} {min_cut_value}\n')


def cut_growth_exclude(n_qubits, depth, circuits_trials, cut_trials):
    
    dat_file_path_circuits = f'results/circuits/qubits{n_qubits}_depth{depth}/circuits.dat'
    dat_file_path_results = f'results/circuits/qubits{n_qubits}_depth{depth}/results_excludes.dat'

    if not os.path.exists(f'results/circuits/qubits{n_qubits}_depth{depth}'):
        os.makedirs(f'results/circuits/qubits{n_qubits}_depth{depth}')

    with open(dat_file_path_results, 'w') as dat_file:
        dat_file.write(f'exclude_nodes min_cut_value\n')

        with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:

            futures = {
                exclude_node: executor.submit(
                    process_trials,
                    n_qubits,
                    depth,
                    [exclude_node] if exclude_node == n_qubits - 1 else [exclude_node, exclude_node + 1],  
                    circuits_trials,
                    cut_trials,
                    dat_file_path_circuits
                ) for exclude_node in range(0, n_qubits-1)
            }
            

            for exclude_node, future in futures.items():
                min_cut_value = future.result()

                dat_file.write(f'{exclude_node} {min_cut_value}\n')






# Unparallelized
# def cut_growth(total_qubits, total_depth, exclude_nodes, trials):
    
#     dat_file_path_circuits = f'results/circuits/qubits{total_qubits}_depth{total_depth}/circuits.dat'
#     dat_file_path_results = f'results/circuits/qubits{total_qubits}_depth{total_depth}/results.dat'
    
#     if not os.path.exists(f'results/circuits/qubits{total_qubits}_depth{total_depth}'):
#         os.makedirs(f'results/circuits/qubits{total_qubits}_depth{total_depth}')
    
#     with open(dat_file_path_results, 'w') as dat_file:
#         dat_file.write(f'qubits depth min_cut_value\n')
#         for n_qubits in range(total_qubits, total_qubits + 1):
#             for depth in range(1, total_depth + 1):
#                 min_cut_values = []
#                 for trial in range(trials):
#                     name = f"{trial}"
#                     qc = random_circuit.random_circuit(n_qubits=n_qubits, depth=depth, name=name, bol_dat=False, dat_file_path=dat_file_path_circuits)
#                     min_cut_value = min_cut.min_cut(qc, exclude_nodes, 10, False, False)
#                     min_cut_values.append(min_cut_value)

#                 min_cut_value = np.mean(min_cut_values)
#                 # save data
#                 dat_file.write(f'{n_qubits} {depth} {min_cut_value}\n')

