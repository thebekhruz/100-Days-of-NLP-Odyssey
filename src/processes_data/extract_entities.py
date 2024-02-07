import pandas as pd
import numpy as np
import spacy
from sklearn.cluster import KMeans


file_path = '/Users/thebekhruz/Desktop/100Days-Of-Code/100-Days-of-NLP-Odyssey/data/raw_data/sample_data.csv'
output_file_path = '/Users/thebekhruz/Desktop/100Days-Of-Code/100-Days-of-NLP-Odyssey/data/processed_data/vectorized_data.csv'




df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])
nlp = spacy.load("en_core_web_lg")



# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Use SpaCy to get word embeddings that capture the semantic meaning
def get_document_embedding(text):
    # Preprocess the text first
    preprocessed_text = preprocess_text(text)
    doc = nlp(preprocessed_text)
    vectors = [token.vector for token in doc if token.has_vector]
    if vectors:
        # Average the vectors to get the document embedding
        document_embedding = np.mean(vectors, axis=0)
    else:
        # If no tokens have vectors, return a zero vector
        document_embedding = np.zeros((nlp.vocab.vectors_length,))
    return document_embedding


def k_cluster(document_embeddings, n_clusters: int):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(document_embeddings)
    return labels, kmeans.cluster_centers_


def get_texts():
    # Directly filter and concatenate 'title' and 'description' rows in one step
    combined = df[df['type'].isin(['title', 'description'])]['value']
    return combined



# Function to preprocess text and extract entities
""" def extract_entities(text):
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
 """
# At this point, df['entities'] contains lists of entity labels extracted from each document
