When you pass a text (like a sentence or a document) to a spaCy model, it converts each word into its corresponding embedding. Then, it typically averages these word embeddings to create a single vector that represents the entire text. This results in capturing the overall semantic meaning of the text, rather than just focusing on specific words or their frequency.

### Contrast with TF-IDF and Bag of Words

- **Bag of Words (BoW)**: This model represents text by counting how many times each word appears. It doesn’t consider the order of words and ignores semantics (word meanings).
    
- **TF-IDF**: It improves upon BoW by considering not just the frequency of a word in a single document but also how unique the word is across all documents (the corpus). It gives more weight to words that are unique to a document, helping to highlight more relevant words.


### Why Embeddings Over BoW or TF-IDF in Semantic Search?

- **Capturing Semantics**: Embeddings are superior for semantic search because they capture more than just word frequency or presence; they capture the context and semantic meaning of words.
    
- **Handling Synonyms**: Embeddings can group synonyms or contextually similar words, which is a limitation in BoW and TF-IDF.
    
- **Dimensionality**: While BoW and TF-IDF result in high-dimensional vectors (depending on the size of the vocabulary), embeddings usually have a fixed and much lower dimensionality, making computations more efficient.


