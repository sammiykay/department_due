import networkx as nx
import matplotlib.pyplot as plt
G_er_updated = nx.DiGraph()

# Add entities and attributes
G_er_updated.add_node("Student", pos=(0, 2))
G_er_updated.add_node("Payment", pos=(2, 1.5))
G_er_updated.add_node("Receipt", pos=(4, 1))
G_er_updated.add_node("Administrator", pos=(0, 0))
G_er_updated.add_node("Dues", pos=(2, 0))
G_er_updated.add_node("Withdraw Cash", pos=(0, -1))

# Add relationships
G_er_updated.add_edges_from([("Student", "Payment"), ("Payment", "Receipt"), ("Administrator", "Dues"), ("Payment", "Dues")])
G_er_updated.add_edge("Administrator", "Withdraw Cash")

# Draw the updated ER diagram
pos_er_updated = nx.get_node_attributes(G_er_updated, 'pos')
plt.figure(figsize=(8, 6))
nx.draw(G_er_updated, pos_er_updated, with_labels=True, node_size=3000, node_color='lightgreen', font_size=10, font_weight='bold', font_color='black', edge_color='grey')

plt.title('Updated ER Diagram with Withdraw Cash Functionality')
plt.show()
