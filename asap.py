import osmnx as ox
import pandas as pd
import ast
from datetime import datetime

# Save the updated graph to a GeoPackage file
ox.io.save_graph_geopackage(
    G,
    filepath='dataset/simplified_directed_2022_GMEL_v3_withallinfo_newclass_newconnections.gpkg',
    directed=True
)

# Load the VISTA node choice set data and process it
df_vista_sa2 = pd.read_csv('P:/cycled_study/VISTA/nodechoicesets_by_landuse_SA2_GMEL_v2.csv')
df_vista_sa2.columns = ['Unnamed: 0', 'MB_CAT21', 'unique_sa2', 'node_choice_set', 'VISTA_place_type']
df_vista_sa2['node_choice_set'] = df_vista_sa2['node_choice_set'].apply(ast.literal_eval)

# Group by SA2 and VISTA place type, and aggregate the node choice sets
df_vista_sa2 = df_vista_sa2.groupby(['unique_sa2', 'VISTA_place_type'])['node_choice_set'].agg(lambda x: sum(x, []))
print('Imported node choice sets')

# Define a sampling rate (X%)
x = 100  # X% of the population-level trips will be sampled

# Create a sampled_num_trips column based on the sampling rate
df_demand['sampled_num_trips'] = (x * df_demand['num_trips'] / 100).round(0)

# Expand the dataframe by repeating rows based on sampled_num_trips
df_demand2 = df_demand.loc[df_demand.index.repeat(df_demand['sampled_num_trips'])].reset_index(drop=True)

# Calculate the spatial distribution of origins and destinations
s2_o = (100 * df_demand2['origsa2'].value_counts() / len(df_demand2)).reset_index()
s2_d = (100 * df_demand2['destsa2'].value_counts() / len(df_demand2)).reset_index()

# Validate that the sampling rate is spatially proportional
df_demand3 = df_demand.loc[df_demand.index.repeat(df_demand['sampled_num_trips'])].reset_index(drop=True)

# Initialize columns for origin and destination nodes, shortest path, etc.
df_demand3['orig_node_r'] = ''
df_demand3['dest_node_r'] = ''
df_demand3['shortest_path_r'] = ''
df_demand3['shortest_path_length_r'] = 0.0
df_demand3['num_attempts'] = 0

# Convert the graph nodes into a list
G_nodes = list(G.nodes())

print('Started OD assignment')
start_time = datetime.now()

# Your code for OD assignment would go here

# End of the OD assignment logic
end_time = datetime.now()
print(f"OD assignment completed in {end_time - start_time}")
