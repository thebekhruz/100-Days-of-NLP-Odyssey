import pandas as pd
import numpy as np
import spacy
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity




# Preprocessing function
def preprocess_text(text):
    text = str(text)
    text = text.lower()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Use Numpy to get word embeddings that capture the semantic meaning
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
    return labels, kmeans


# def get_key_vocabulary(nlp, limit=10000):
#     """Generate a list of key vocabulary and their vectors."""
#     words = [word for word in nlp.vocab.strings]
#     words = words[:limit]  # Limit to the first N words for efficiency
#     vectors = np.array([nlp.vocab[word].vector for word in words if nlp.vocab[word].has_vector])
#     return words, vectors


def get_dataset_words_to_vectors(texts, nlp):
    """Create a mapping of unique words in the dataset to their vectors."""
    unique_words = set()
    for doc in nlp.pipe(texts, disable=["parser", "ner"]):
        unique_words.update([token.lemma_ for token in doc if token.has_vector and not token.is_stop and not token.is_punct])
    
    # Map words to their vectors
    word_to_vector = {word: nlp.vocab[word].vector for word in unique_words}
    return word_to_vector

def find_top_words_for_clusters(kmeans, word_to_vector, top_n=10):
    vectors = np.array(list(word_to_vector.values()))
    words = list(word_to_vector.keys())
    top_words_per_cluster = []
    
    for center in kmeans.cluster_centers_:
        # Calculate cosine similarity and get top N indices
        similarities = cosine_similarity(center.reshape(1, -1), vectors)
        top_indices = similarities.argsort()[0][-top_n:][::-1]
        
        # Fetch top words for the cluster
        top_words = [words[index] for index in top_indices]
        top_words_per_cluster.append(top_words)
    
    return top_words_per_cluster



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
    labels, kmeans = k_cluster(embeddings, n_clusters)
    
    # Map labels back to original DataFrame
    texts_and_ids['cluster'] = labels
    
    # Prepare the output DataFrame, ensuring no duplication
    output_df = texts_and_ids[['doc_id', 'cluster']].drop_duplicates()
    
    # Get word to vector mapping for dataset-specific words
    word_to_vector = get_dataset_words_to_vectors(df['value'], nlp)
    
    # Find top words for each cluster
    top_words_per_cluster = find_top_words_for_clusters(kmeans, word_to_vector, top_n=10)
    
    # Print top words for each cluster for interpretation
    for i, words in enumerate(top_words_per_cluster):
        print(f"Cluster {i}: {', '.join(words)}\n")
    
    # Write the output DataFrame to a file
    # try:
    #     output_df.to_csv(output_file_path, index=False, sep='\t', header=True)
    #     print("Output has been saved to: \n\n" + output_file_path + "\n")
    # except Exception as e:
    #     print(f"Error occurred while writing to file: {e}")



# def main(file_path, output_file_path, n_clusters):
#     df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])
#     texts_and_ids = get_texts_and_ids(df)

#     # Generate embeddings
#     texts_and_ids['embedding'] = texts_and_ids['value'].apply(get_document_embedding)

#     # Cluster the embeddings
#     embeddings = np.vstack(texts_and_ids['embedding'].values)
#     labels, kmeans = k_cluster(embeddings, n_clusters)

#     # Find top N words for each cluster
#     top_words_per_cluster = find_top_words_for_clusters(kmeans, nlp, top_n=10)

#     # Print top words for each cluster
#     for i, words in enumerate(top_words_per_cluster):
#         print(f"Cluster {i}: {', '.join(words)}\n \n")


    # # Map labels back to original DataFrame
    # texts_and_ids['cluster'] = labels

    # # Prepare the output DataFrame, ensuring no duplication
    # output_df = texts_and_ids[['doc_id', 'cluster']].drop_duplicates()

    # # Write the output DataFrame to a file
    # try:
    #     output_df.to_csv(output_file_path, index=False, sep='\t', header=True)
    #     print("Output has been saved to: \n\n" + output_file_path + "\n")
    # except Exception as e:
    #     print(f"Error occurred while writing to file: {e}")



nlp = spacy.load("en_core_web_lg")

file_path = 'data/raw_data/sample_data.csv'
output_file_path = 'data/processed_data/vectorized_data.csv'
n_clusters = 10 # Number of clusters to use
main(file_path, output_file_path, n_clusters)

