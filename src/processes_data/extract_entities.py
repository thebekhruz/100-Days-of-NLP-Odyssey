import pandas as pd
import numpy as np
import spacy
from sklearn.cluster import KMeans




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


def get_texts_and_ids(df):
    # Return both 'doc_id' and 'value' for filtering
    filtered = df[df['type'].isin(['title', 'description'])][['doc_id', 'value']]
    return filtered

def main(file_path, output_file_path, n_clusters):
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])
    texts_and_ids = get_texts_and_ids(df)

    # Generate embeddings
    texts_and_ids['embedding'] = texts_and_ids['value'].apply(get_document_embedding)

    # Cluster the embeddings
    embeddings = np.vstack(texts_and_ids['embedding'].values)
    labels, _ = k_cluster(embeddings, n_clusters)

    # Map labels back to original DataFrame
    texts_and_ids['cluster'] = labels

    # Prepare the output DataFrame, ensuring no duplication
    output_df = texts_and_ids[['doc_id', 'cluster']].drop_duplicates()

    # Write the output DataFrame to a file
    try:
        output_df.to_csv(output_file_path, index=False, sep='\t', header=True)
        print("Output has been saved to: \n\n" + output_file_path + "\n")
    except Exception as e:
        print(f"Error occurred while writing to file: {e}")



nlp = spacy.load("en_core_web_lg")

file_path = 'data/raw_data/sample_data.csv'
output_file_path = 'data/processed_data/vectorized_data.csv'
n_clusters = 10 # Number of clusters to use
main(file_path, output_file_path, n_clusters)

