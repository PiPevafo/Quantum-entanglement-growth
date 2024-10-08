import networkx as nx 
import matplotlib.pyplot as plt 
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Function to plot the circuit graph
def draw_circuit_graph(G, pos, name = None, u = None, v = None):
        
    plt.figure(figsize=(7, 7))
    node_colors = [G.nodes[node].get('color', 'lightgreen') for node in G.nodes()]
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_color=node_colors, edge_color="black", node_size=800, font_size=9, font_weight="bold", width=2)
    
    if u is not None and v is not None:
        
        base_name = ''.join(filter(str.isalpha, name))
        if not os.path.exists(f'results/graphs/min_cut_{base_name}'):
            os.makedirs(f'results/graphs/min_cut_{base_name}')
            
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Circuit " + name + " before merge the nodes " + str(u) + " y " + str(v))
        path = f'results/graphs/min_cut_{base_name}/{name}.png'
    
    else:
        if name is None:
            name = "circuit"
        plt.title("Graph Representing the Circuit " + name )
        path = f'results/{name}.png'
    
    plt.savefig(path)
    plt.close()  
    # plt.show()


# Funcion to convert a quantum circuit to a graph

def circuit_to_graph(qc):
    n_qubits = qc.num_qubits

    # Create a graph
    G = nx.Graph()
    name = qc.name
    if name is None:
        name = "Circuit"
        
    # Add nodes for the qubits and the top nodes (final qubits) for each initial qubit
    qubit_top_nodes = []
    for qubit in range(n_qubits):
        qubit_top_node = f'q_top_{qubit}'
        G.add_node(f'q_{qubit}', label=f'q_{qubit}')
        G.add_node(qubit_top_node, label=f'q_{qubit}')
        qubit_top_nodes.append(qubit_top_node)  
            
    # Add nodes and edges for two-qubit gates with unique identifiers
    gate_counter = 0
    previous_gate_nodes = {}
    gate_colors = {
        'cx': 'skyblue',
        'cz': 'red',
        'swap': 'green',
        # Add more colors for other gates if needed
    }
    
    for gate, qubits, clbits in qc.data:
        if gate.name in gate_colors: 
            qubit_indices = [qc.qubits.index(qubit) for qubit in qubits]
            gate_id = f'{gate.name.upper()}-{gate_counter}'
            G.add_node(gate_id, label=f'{gate.name.upper()}-{gate_counter}', index=gate_counter, color=gate_colors[gate.name])
                
            for qubit_index in qubit_indices:
                if qubit_index in previous_gate_nodes:
                    G.add_edge(gate_id, previous_gate_nodes[qubit_index], weight=1)
                else:
                    G.add_edge(gate_id, f'q_{qubit_index}', weight=1)
                previous_gate_nodes[qubit_index] = gate_id
            
            gate_counter += 1

    # Connect the last nodes of the gates to the upper qubits
    for qubit_index in range(n_qubits):
        if qubit_index in previous_gate_nodes:
            G.add_edge(previous_gate_nodes[qubit_index], f'q_top_{qubit_index}')
        else:
            # If there is no associated gate node, directly connect the lower qubit to the upper qubit
            G.add_edge(f'q_{qubit_index}', f'q_top_{qubit_index}', weight=1)

    # Set the position of the nodes
    pos = {}
    
    # Positions of qubits in a row at the bottom
    for i in range(n_qubits):
        pos[f'q_{i}'] = (i, 0)
        pos[f'q_top_{i}'] = (i, gate_counter + 2)  # Positions of the higher qubits

    # Gate positions in upper rows
    gate_counter = 0
    for gate, qubits, clbits in qc.data:
        if gate.name in gate_colors:
            qubit_indices = [qc.qubits.index(qubit) for qubit in qubits]
            gate_id = f'{gate.name.upper()}-{gate_counter}'
            pos[gate_id] = (sum(qubit_indices) / len(qubit_indices), gate_counter + 1)
            gate_counter += 1

    return G, pos, qubit_top_nodes, name


#create animation of the karger algorithm
def cut_animation(path, name):


    image_files = sorted([f for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg')], 
                        key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    fig_size=(7, 7)
    fig = plt.figure(figsize=fig_size)
    
    def update_image(i):
        img = Image.open(os.path.join(path, image_files[i]))
        
        img_size=(500, 500)
        img = img.resize(img_size)

        plt.imshow(img)
        plt.axis('off')  

    ani = animation.FuncAnimation(fig, update_image, frames=len(image_files), repeat=True)

    ani.save(f'results/{name}.gif', writer='imagemagick', fps=2)  
