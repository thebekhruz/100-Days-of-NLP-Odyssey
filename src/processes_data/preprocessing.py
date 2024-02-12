import pandas as pd
import spacy

# Load the SpaCy model with specific components disabled for efficiency
nlp = spacy.load("en_core_web_md", disable=["ner", "parser"])

def preprocess_text(doc):
    """
    Preprocess a single document by tokenizing, converting to lowercase,
    lemmatizing, removing stopwords, and punctuation.
    """
    # Tokenization happens implicitly here; each `token` is a result of tokenization
    return " ".join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)

def preprocess_texts_in_batches(texts, batch_size=256):
    """
    Process texts in batches, applying preprocessing steps included
      in preprocess_text function.
    """
    processed_texts = []
    # The nlp.pipe method handles tokenization as part of processing
    for doc in nlp.pipe(texts, batch_size=batch_size):
        processed_texts.append(preprocess_text(doc))
    return processed_texts

def get_texts_with_ids(df, text_type):
    """Get texts and their doc_ids based on type (title/description)."""
    relevant_df = df[df['type'] == text_type]
    return relevant_df['doc_id'].tolist(), relevant_df['value']

def save_processed_data(doc_ids, processed_texts, output_file_path):
    """Save processed texts with their doc_ids to a CSV file."""
    processed_df = pd.DataFrame({'doc_id': doc_ids, 'value': processed_texts})
    processed_df.to_csv(output_file_path, sep='\t', index=False, header=None)

def main():
    file_path = 'data/raw_data/sample_data.csv'
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

    # Process and save titles
    title_ids, titles = get_texts_with_ids(df, 'title')
    processed_titles = preprocess_texts_in_batches(titles)
    save_processed_data(title_ids, processed_titles, 'data/processed_data_title.csv')

    # Process and save descriptions
    description_ids, descriptions = get_texts_with_ids(df, 'description')
    processed_descriptions = preprocess_texts_in_batches(descriptions)
    save_processed_data(description_ids, processed_descriptions, 'data/processed_data_descr.csv')

if __name__ == '__main__':
    main()
