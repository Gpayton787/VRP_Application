#Create a DAG object

import networkx as nx
import matplotlib.pyplot as plt
from pdf_extracter import create_trip_dict

data = create_trip_dict("trips.pdf")
trip_dict = data["trips"]
# print(trip_dict)

G = nx.DiGraph()

for i, trip in enumerate(trip_dict):
    G.add_node(i, pick_up = (trip["pick_up_time"], trip["pick_up_location"]))
    G.add_node((i+0.1), drop_off = (trip["drop_off_time"], trip["drop_off_location"]))
    G.add_weighted_edges_from([(i, (i+0.1), 5)])

print(len(trip_dict))
print(G)

    
# Add nodes and edges
plt.figure(figsize=(6, 4))
pos = nx.circular_layout(G)  # Positions nodes in a circular layout
labels = nx.get_edge_attributes(G, 'weight')  # Get edge weights as labels
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Display edge weights
plt.title('Directed Graph with Weighted Edges')
plt.show()
