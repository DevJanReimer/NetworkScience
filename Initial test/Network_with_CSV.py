import numpy as np
import pandas as pd
import os
import networkx as nx

#Ind1: % of Import Reporter from Partner
#Ind2: % of Export Reporter to Partner
#Ind3: % of Import Partner form Reporter
#Ind4: % of Export Partner to Reporter

# Step 1: Check current directory
print("Current Directory:", os.getcwd())

# Step 2: Set a new directory
new_directory = r"C:\Users\mathi\OneDrive\Desktop\Volkswirtschaft - Studium\Master\3. Semester\Network Science\Project Studies"  # Replace this with your desired path
os.chdir(new_directory)

# Step 3: Confirm the change
print("New Directory:", os.getcwd())

# Step 1: Load the 'data' CSV file
data = pd.read_csv("data.csv")

# Step 2: Filter for "L3" == "T03"
data_filtered = data[data["L3"] == "T03"]

# Step 3: Create a new variable "ExportRP"
data_filtered["ExportRP"] = data_filtered["Partner_Total_Imports"] * data_filtered["Ind3"]

# Step 4: Keep only "Reporter", "Partner", and "ExportRP"
data_filtered = data_filtered[["Reporter", "Partner", "ExportRP"]]

# Step 5: Load the 'other_economy' CSV file
other_economy = pd.read_csv("other_economy.csv")

# Clean the "PartnerName" column
def clean_partner_name(name):
    # Remove quotation marks and keep only the part before the comma
    if pd.notnull(name):  # Check if name is not NaN
        name = name.strip('"')  # Remove surrounding quotation marks
        return name.split(",")[0].strip()  # Split by comma, take first part, and strip whitespace
    return name  # If NaN, return as is

other_economy["PartnerName"] = other_economy["PartnerName"].apply(clean_partner_name)

# Step 6: Replace "Reporter" and "Partner" in the `data` DataFrame
# Assuming "Partner" in `data` corresponds to "Partner" in `other_economy` and we use "PartnerName" for the replacement
partner_mapping = other_economy.set_index("Partner")["PartnerName"].to_dict()

# Replace "Reporter" and "Partner" in `data_filtered`
data_filtered["Reporter"] = data_filtered["Reporter"].map(partner_mapping)
data_filtered["Partner"] = data_filtered["Partner"].map(partner_mapping)

# Step 7: Display or save the cleaned dataset
print(data_filtered.head())  # Preview the result
data_filtered.to_csv("cleaned_data.csv", index=False)  # Save the cleaned dataset to a new CSV file

# Load the cleaned dataset
cleaned_data = pd.read_csv("cleaned_data.csv")

# Initialize a directed graph
graph = nx.DiGraph()

# Add edges with weights to the graph
for _, row in cleaned_data.iterrows():
    reporter = row["Reporter"]
    partner = row["Partner"]
    weight = row["ExportRP"]

    # Add nodes and edges
    graph.add_edge(reporter, partner, weight=weight)

# Export the graph to a .gml file
output_file = "trade_network.gml"
nx.write_gml(graph, output_file)

print(f"Graph exported to {output_file}")


