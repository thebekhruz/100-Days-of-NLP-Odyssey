import time
import pandas as pd
import spacy
import re
from dateutil.parser import parse

# Load the SpaCy model with specific components disabled for efficiency
nlp = spacy.load("en_core_web_md", disable=["ner", "parser"])

# Corrected Abbreviations map
abbreviation_expansions = {
    # Compass directions
    "N": "North",
    "S": "South",
    "E": "East",
    "W": "West",
    "NE": "Northeast",
    "NW": "Northwest",
    "SE": "Southeast",
    "SW": "Southwest",
    # Street Names
    "St": "Street",
    "Rd": "Road",
    "Ave": "Avenue",
    "Dr": "Drive",
    "Blvd": "Boulevard",
    "Ln": "Lane",
    "Ct": "Court",
    "Pl": "Place",
    "Sq": "Square",
    "Ter": "Terrace",
    "Cir": "Circle",
    # Geographical locations (examples)
    "US": "United States",
    "UK": "United Kingdom",
    "CA": "California",
    "NY": "New York",
    # Dates
    "c.": "circa", "c" : "circa",
    "Mon.": "Monday ", "Mon": "Monday",
    "Tue.": "Tuesday ", "Tue": "Tuesday",
    "Wed.": "Wednesday ", "Wed": "Wednesday",
    "Thu.": "Thursday ", "Thu": "Thursday",
    "Fri.": "Friday ", "Fri": "Friday",
    "Sat.": "Saturday ", "Sat": "Saturday",
    "Sun.": "Sunday ", "Sun": "Sunday",
    "Jan.": "January ", "Jan": "January ",
    "Feb.": "February ", "Feb": "February",
    "Mar.": "March ", "Mar": "March",
    "Apr.": "April ", "Apr": "April",
    "May": "May",
    "Jun.": "June ", "Jun": "June",
    "Jul.": "July ", "Jul": "July",
    "Aug.": "August ", "Aug": "August",
    "Sep.": "September ", "Sep": "September ", "Sept.": "September ", "Sept": "September ",
    "Oct.": "October ", "Oct": "October",
    "Nov.": "November ", "Nov": "November",
    "Dec.": "December ", "Dec": "December"
    # Extend this list as needed
}

def expand_abbreviations(text, abbreviation_expansions):
    """
    Replace abbreviations in the text with their expanded forms using regex to match whole words.
    """
    for abbr, expansion in abbreviation_expansions.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', expansion, text, flags=re.IGNORECASE)
    return text



def preprocess_text(text):
    """
    Preprocess a single document by expanding abbreviations, tokenizing, converting to lowercase,
    lemmatizing, removing stopwords, and punctuation.
    """
    # Replace underscores with spaces
    text = text.replace('_', ' ')
    
    expanded_text = expand_abbreviations(text, abbreviation_expansions)
    doc = nlp(expanded_text)
    return " ".join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)

def preprocess_texts_in_batches(texts, batch_size=256):
    """
    Expand abbreviations and process texts in batches, applying preprocessing steps.
    """
    texts = [text if isinstance(text, str) else '' for text in texts]

    processed_texts = []
    for doc in nlp.pipe([expand_abbreviations(text, abbreviation_expansions) for text in texts], batch_size=batch_size):
        processed_text = " ".join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)
        processed_texts.append(processed_text)
    return processed_texts


def get_texts_with_ids(df, text_type):
    """Get texts and their doc_ids based on type (title/description)."""
    relevant_df = df[df['type'] == text_type]
    return relevant_df['doc_id'].tolist(), relevant_df['value'].tolist()

def save_processed_data(doc_ids, processed_texts, output_file_path, types):
    """Save processed texts with their doc_ids to a CSV file."""
    processed_df = pd.DataFrame({'doc_id': doc_ids, 'type': types, 'value': processed_texts})
    processed_df.to_csv(output_file_path, sep='\t', index=False, header=None)

def main():
    start_time = time.time()  # Start time measurement

    # file_path = 'data/raw_data/partitions/partition_2500ent.csv'
    file_path = 'data/raw_data/swop_triples.csv'
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

    # Process and save titles
    output_file_path_titles = 'data/processed_data/processed_data_title.csv'
    title_ids, titles = get_texts_with_ids(df, 'title')
    processed_titles = preprocess_texts_in_batches(titles)  # No need to convert to list, it's already a list from get_texts_with_ids
    save_processed_data(title_ids, processed_titles, output_file_path_titles, 'title')

    # Process and save descriptions
    output_file_path_desc = 'data/processed_data/processed_data_descr.csv'
    description_ids, descriptions = get_texts_with_ids(df, 'description')
    processed_descriptions = preprocess_texts_in_batches(descriptions)
    save_processed_data(description_ids, processed_descriptions, output_file_path_desc, 'description')

    end_time = time.time()  # End time measurement
    print(f"\nSuccess! \nExecution Time: {end_time - start_time} seconds")  # Print execution time 

if __name__ == '__main__':
    main()