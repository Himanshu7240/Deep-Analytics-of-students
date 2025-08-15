import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import os

print("--- Peer Influence Tracking using Social Network Analysis ---")

# --- Step 1: Load and Prepare Data ---
print("\nStep 1: Loading student, academic, and relational data...")

# Robust path detection for data directory
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from peer_influence_analysis subdirectory
        './data/'          # If data is in current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found data directory at: {path}")
            return path
    
    raise FileNotFoundError("Data directory not found. Please ensure the 'data/' folder exists.")

# Find the data directory
base_path = find_data_directory()

# Load the datasets
df_students = pd.read_csv(base_path + 'student_master.csv')
df_academic = pd.read_csv(base_path + 'academic_performance.csv')
df_relational = pd.read_csv(base_path + 'relational_social.csv')
print("Data loaded.")

# Get script directory for saving images
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Step 2: Synthesize Peer Connections (Graph Edges) ---
# We simulate group projects by creating random groups within each class.
print("Step 2: Synthesizing peer connections from class rosters...")

# Use the most recent term for the network
latest_term = 'Spring 2025'
df_term_relations = df_relational[df_relational['term'] == latest_term]

edges = []
# Group students by the class they share
for course_id, group in df_term_relations.groupby('course_id'):
    class_roster = list(group['student_id'].unique())
    random.shuffle(class_roster) # Randomize for group creation
    
    # Create small project groups of 3 or 4
    group_size = random.choice([3, 4])
    for i in range(0, len(class_roster), group_size):
        project_group = class_roster[i:i + group_size]
        # In a group, everyone is connected to everyone else
        # Create all pairs (edges) within the group
        for u, v in itertools.combinations(project_group, 2):
            edges.append((u, v))

print(f"Synthesized {len(edges)} peer connections (edges) for the network.")

# --- Step 3: Build the Network Graph with networkx ---
print("Step 3: Building the student network graph...")
G = nx.Graph()

# Add all students as nodes in the graph
for _, student in df_students.iterrows():
    G.add_node(student['student_id'], name=f"{student['first_name']} {student['last_name']}")

# Add the synthesized connections as edges
G.add_edges_from(edges)

# --- Step 4: Add Academic Performance as Node Attributes ---
# This allows us to color-code the network by performance.
print("Step 4: Enriching the network with academic data...")
df_latest_academic = df_academic[df_academic['term'] == latest_term]

performance_attributes = {}
for _, student_row in df_latest_academic.iterrows():
    student_id = student_row['student_id']
    score = student_row['final_score']
    
    # Categorize performance
    if score >= 85:
        category = 'High-Performing'
    elif score >= 70:
        category = 'Average-Performing'
    else:
        category = 'At-Risk'
        
    performance_attributes[student_id] = {'performance': category, 'score': score}

# Add these attributes to the nodes in our graph
nx.set_node_attributes(G, performance_attributes)

# --- Step 5: Visualize the Network ---
print("Step 5: Visualizing the peer network. Please close the plot window to exit.")
plt.figure(figsize=(18, 18))

# Define colors for performance categories
color_map = {'High-Performing': 'skyblue', 'Average-Performing': 'lightgreen', 'At-Risk': 'salmon'}
node_colors = [color_map.get(G.nodes[n].get('performance', 'grey'), 'grey') for n in G.nodes()]

# Use a layout algorithm to position nodes
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the network
nx.draw(G, pos, 
        with_labels=True, 
        node_color=node_colors, 
        node_size=1500, 
        font_size=10, 
        font_weight='bold',
        edge_color='gray',
        width=0.5)

# Create a legend
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=category, 
                             markerfacecolor=color, markersize=15) for category, color in color_map.items()]
plt.legend(handles=legend_handles, title='Performance Level', loc='upper right')

plt.title(f'Student Peer Network for {latest_term}', size=20)
plt.savefig(os.path.join(script_dir, 'student_peer_network.png'))
print("Saved chart: student_peer_network.png")
plt.show()

print("\n--- Process Complete ---")