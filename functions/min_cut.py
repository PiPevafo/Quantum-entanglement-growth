import numpy as np

from functions import modified_karger_algorithm

#Execute the algoritm 

def min_cut(qc, exclude_nodes, trials, bool_cuts = None, bool_plot = None):
    
    if bool_plot is None:
        bool_plot = False
    else:
        cut = modified_karger_algorithm.karger_min_cut_circuit(qc, exclude_nodes, bool_plot)
    
    cuts = []
    min_cut = float('inf')

    for _ in range(trials):
        cut = modified_karger_algorithm.karger_min_cut_circuit(qc, exclude_nodes, False)
        cuts.append(cut)
        min_cut = min(cut, min_cut)
         
    print(f"The minimum cut passing through the quitbs {exclude_nodes} is: {min_cut}")
    
    if bool_cuts is not None and bool_cuts is True:
        print("The total cuts made are ", cuts)