import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'un_comtrade_free_api_data.csv'  # Replace with your file path
trade_data = pd.read_csv(file_path)

# Extract relevant columns for the network
network_data = trade_data[["reporterCode", "partnerCode", "primaryValue"]].dropna()

# Rename columns for clarity
network_data.columns = ["source", "target", "weight"]

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph
for _, row in network_data.iterrows():
    G.add_edge(row["source"], row["target"], weight=row["weight"])

# Save the graph to a GML file
gml_path = "trade_network.gml"  # Specify your desired output path
nx.write_gml(G, gml_path)

# Print graph details
print(f"Graph saved as: {gml_path}")
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Visualize the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)  # Use spring layout for node positioning
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='blue', alpha=0.7)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title("Trade Network Graph")
plt.show()