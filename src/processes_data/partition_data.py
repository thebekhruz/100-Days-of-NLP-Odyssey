import pandas as pd
import numpy as np

# Load the data
file_path = 'data/raw_data/swop_triples.csv'
df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

# Group the data by 'doc_id'
grouped = df.groupby('doc_id')
# print(len(grouped))   # 42986

# Number of random groups to select
n = 1500  # n = 500; means rougly 2500 entries

# Randomly select 'n' groups
if n > len(grouped):
    print(f"Requested number of groups exceeds the total number of unique 'doc_id's. Adjusting to {len(grouped)}.")
    n = len(grouped)
    
selected_groups = grouped.apply(lambda x: x.sample(1))  # This ensures we're sampling from unique groups
selected_indices = np.random.choice(selected_groups.index.levels[0], size=n, replace=False)
selected_data = df[df['doc_id'].isin(selected_indices)]

# Export the selected groups to a new CSV, inserting empty lines between them
output_file_path = 'data/raw_data/chunk/partition_2500ent.csv'
with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
    for _, group in selected_data.groupby('doc_id'):
        group.to_csv(f, sep='\t', index=False, header=False)
        f.write('\n')  # Insert an empty line between groups

print(f"\nData successfully partitioned into {output_file_path}")
