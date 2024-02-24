import spacy
import numpy as np


# Example text
dataset = [
    "The Eiffel Tower is a wrought iron lattice tower on the Champ de Mars in Paris, France.",
    "The theory of relativity was developed by Albert Einstein, revolutionizing theoretical physics.",
    "Shakespeare's play Romeo and Juliet is a tragedy about two young star-crossed lovers.",
    "The Great Wall of China is a series of fortifications made of stone, brick, and other materials.",
    "Photosynthesis is the process used by plants, algae, and some bacteria to harness sunlight into chemical energy."
]


# Load the spaCy model
nlp = spacy.load("en_core_web_md") 

# Function to encode texts to vectors
def encode_texts(texts):
    return np.array([nlp(text).vector for text in texts])

# Encode our dataset
encoded_dataset = encode_texts(dataset)

# Semantic search function
def semantic_search(query, dataset, encoded_dataset):
    query_vector = nlp(query).vector
    similarities = np.dot(encoded_dataset, query_vector)
    most_similar = dataset[np.argmax(similarities)]
    return most_similar

# Example query
query = "dramatic love story"
result = semantic_search(query, dataset, encoded_dataset)
print("Most similar text to your query:", result)