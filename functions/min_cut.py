import networkx as nx

from functions import modified_karger_algorithm, draw_graph

def draw_minimal_cut(G, pos, name, path):
    
    iteration = 0
    for cut in path:
        G = modified_karger_algorithm.merge_nodes(G, cut[0], cut[1])    
        draw_graph.draw_circuit_graph(G, pos, f'{name}_{iteration}', cut[0], cut[1])
        iteration += 1
        
    draw_graph.cut_animation("results/graphs/min_cut_prueba", f'{name}_animation')

#Execute the algoritm to obtain the better cut

def min_cut(qc, exclude_nodes, trials, bool_cuts = None, bool_plot = None):
    
    min_path = []
    cuts = []
    min_cut = float('inf')

    for _ in range(trials):
        cut, path, G, pos, name = modified_karger_algorithm.karger_min_cut_circuit(qc, exclude_nodes, False)
        cuts.append(cut)
        if cut < min_cut:
            min_cut = cut
            min_path = path
    
    if min_cut >= 100000:
        while min_cut >= 100000:
            cut, path, G, pos, name = modified_karger_algorithm.karger_min_cut_circuit(qc, exclude_nodes, False)
            cuts.append(cut)
            if cut < min_cut:
                min_cut = cut
                min_path = path
        
           
    if bool_cuts is not None and bool_cuts is True:
        print(f"The minimum cut passing through the quitbs {exclude_nodes} is: {min_cut}")
        print("The total cuts made are ", cuts)
        
    if bool_plot is not None and bool_plot is True:
        draw_minimal_cut(G, pos, name, min_path)

    return min_cut




