#Create a DAG object

import networkx as nx
import matplotlib.pyplot as plt
from pdf_extracter import create_trip_dict

trip_dict = create_trip_dict("trips.pdf")
print (len(trip_dict))
G = nx.DiGraph()
for trip in trip_dict:
    G.add_node(trip["id"], name=trip["name"], pick_up_time=trip["pick_up_time"], pick_up_location=trip["pick_up_location"], drop_off_time=trip["drop_off_time"], drop_off_location=trip["drop_off_location"])

pos = nx.spring_layout(G)  # Define the positions of nodes
nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_weight='bold', arrows=True)
plt.title("Vehicle Routing Problem Graph")
plt.show()
plt.savefig("graph.png")
plt.close()