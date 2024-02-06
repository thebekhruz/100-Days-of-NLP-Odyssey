import pandas as pd
import spacy


file_path = '/Users/thebekhruz/Desktop/100Days-Of-Code/100-Days-of-NLP-Odyssey/data/raw_data/sample_data.csv'
# Specify your new output file path
output_file_path = '/Users/thebekhruz/Desktop/100Days-Of-Code/100-Days-of-NLP-Odyssey/data/processed_data/vectorized_data.csv'


df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])


# Load spaCy model with NER
nlp = spacy.load("en_core_web_sm")

# Function to preprocess text and extract entities
def extract_entities(text):
    doc = nlp(text)
    entities = set()  # Use a set to avoid duplicate entities
    for ent in doc.ents:
        entities.add(ent.label_)  # Add entity label as potential category
    return list(entities)  # Convert set back to list

description_rows = df[df['type'] == 'description']
description_rows = description_rows['value']

title_rows = df[df['type'] == 'title']
title_rows = title_rows['value']

# Combine title_rows with description_rows
combined = pd.concat([title_rows, description_rows])
# print(combined.head(10))


df['entities'] = combined.apply(lambda x: extract_entities(str(x)))


# df['category'] = df['entities'].apply(lambda x: max(set(x), key=x.count) if x else 'Unknown')
df['category'] = df['entities'].apply(lambda x: max(set(x), key=x.count) if isinstance(x, list) and x else 'Unknown')


# show first 10 entities
print(df['category'].head())

# At this point, df['entities'] contains lists of entity labels extracted from each document
