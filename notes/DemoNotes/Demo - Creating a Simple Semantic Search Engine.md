## Summary

A simple semantic search engine can be developed by converting data and search queries into vector forms, using either word embeddings or another method. The similarity between the query vector and data vectors is measured using cosine similarity or dot product, with the dot product method requiring normalised vectors. The most relevant data is then identified using the `argmax` function.

> In the provided semantic search example using spaCy, preprocessing steps are not explicitly performed because spaCy's models inherently handle many aspects of text normalisation and understanding.

### Steps for Semantic Search Engine Creation

1. **Vector Conversion**: Convert data into vector form, possibly using word embeddings. Refer to [Word Embeddings in spaCy](https://chat.openai.com/g/g-CDjGiCqI2-notes-gpt/c/Word%20Embeddings%20in%20spaCy) for implementation.
2. **Query Vectorization**: Convert search queries into vector form.
3. **Similarity Measurement**:
    - Use cosine similarity or dot product to measure the similarity between query vectors and data vectors.
    - Note: When using dot product, ensure vectors are normalized.
4. **Identifying Best Match**:
    - Apply the `argmax` function to determine the data vector that best matches the query vector.


