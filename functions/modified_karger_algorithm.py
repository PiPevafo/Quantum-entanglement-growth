import networkx as nx 
import matplotlib.pyplot as plt 
import random

from functions import draw_graph

# Function to merge two nodes in a graph
def merge_nodes(G, node1, node2):
    
    G = G.copy()
    
    # Make sure both nodes exist in the graph
    if node1 not in G.nodes or node2 not in G.nodes:
        raise ValueError(f"One or both nodes ({node1}, {node2}) are not in the graph.")
    
    # Get common neighbors between node1 and node2
    common_nodes = sorted(nx.common_neighbors(G, node1, node2))

    new_edges_weights = []
    
    for node in common_nodes:
        weight_sum = G[node1][node].get('weight', 1) + G[node2][node].get('weight', 1)
        new_edges_weights.append([node, weight_sum])
    
    G = nx.contracted_nodes(G, node1, node2, self_loops=False)
    new_node = node1
    
    # Update the weights of the incident edges to the new node
    for neighbor, weight_info in zip(common_nodes, new_edges_weights):
        neighbor_node = weight_info[0]
        weight_sum = weight_info[1]
        G[new_node][neighbor_node]['weight'] = weight_sum
    
    return G


# Define the modified Karger's algorithm function for a quantum circuit

def karger_min_cut_circuit(qc, exclude_nodes, bool_plot = None):
        
    G, pos, qubit_top_nodes, name = draw_graph.circuit_to_graph(qc)
    
    G = G.copy()  # Copy the graph to avoid modifying the original graph
    
    if exclude_nodes is None:
        exclude_nodes = []
    
    # Add an edge with weight 0 between the two excluded nodes 
    
    exclude_nodes = [f'q_top_{node}' for node in exclude_nodes]
    G.add_edge(exclude_nodes[0], exclude_nodes[1], weight=0)    

    # # Add an edge with a large weight between the top left qubit and the first initial qubit,
    # and also for the top right qubit and the final initial qubit

    G.add_edge(f'q_0', qubit_top_nodes[0], weight=1000)
    G.add_edge(f'q_{qc.num_qubits - 1}', qubit_top_nodes[qc.num_qubits -1], weight=1000)

    # Merge the top qubits with the adjacent excluded qubit
    
    for i in range(len(qubit_top_nodes) - 2):
    
        qubit_top_node = qubit_top_nodes[i]
        qubit_top_node_num = int(qubit_top_node.split('_')[-1])
        
        if qubit_top_node_num < int(exclude_nodes[0].split('_')[-1]):
            node_to_merge = f'q_top_{qubit_top_node_num + 1}'
            if node_to_merge in G and qubit_top_node in G:
                G = merge_nodes(G, node_to_merge, qubit_top_node)
            
        else:
            qubit_top_node = qubit_top_nodes[i +2]
            if exclude_nodes[1] in G and qubit_top_node in G:
                G = merge_nodes(G, exclude_nodes[1], qubit_top_node)

    iteration = 1
    
        
    # While there are more than two nodes in the graph
    
    while len(G.nodes) > 2:
        
        
        if len(G.nodes) == 3:

            u = random.choice(exclude_nodes)
            v = next(node for node in G.nodes if node not in exclude_nodes)
            
            if bool_plot is not None and bool_plot == True: 
                draw_graph.draw_circuit_graph(G, pos, f"{name}_{iteration}" , u, v)
        
        else:   
            # Filter edges that do not involve the excluded nodes
            edges = [(u, v) for u, v in list(G.edges) if u not in exclude_nodes or v not in exclude_nodes]

            u, v = random.choice(edges)
            if v == exclude_nodes[0] or v == exclude_nodes[1]:
                u, v = v, u
                
            if bool_plot is not None and bool_plot == True: 
                draw_graph.draw_circuit_graph(G, pos, f"{name}_{iteration}", u, v)
            
        G = merge_nodes(G, u, v)
        
        iteration += 1

    if bool_plot is not None and bool_plot == True: 
        draw_graph.draw_circuit_graph(G, pos, f"{name}_{iteration}", u, v)
        
    # Finding the two remaining nodes and calculate the total weight of the edges between them
    
    remaining_nodes = list(G.nodes)
    u, v = remaining_nodes
    
    cut_weight = G[u][v].get('weight', 1)
    
    return cut_weight

