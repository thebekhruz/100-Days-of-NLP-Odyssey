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
    # for abbr, expansion in abbreviation_expansions.items():
    #     # Use the \b metacharacter to ensure we're only matching whole words
    #     text = re.sub(r'\b' + re.escape(abbr) + r'\b', expansion, text)
    # return text

    for abbr, expansion in abbreviation_expansions.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', expansion, text, flags=re.IGNORECASE)
    return text

# def standardize_date(text):
#     """
#     Search for dates within the text and convert them to ISO 8601 format (YYYY-MM-DD).
#     This function now tries to identify more general date formats using dateutil for parsing.
#     """
#     # Improved regex pattern to match a wider range of date formats
#     date_pattern = re.compile(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{1,2},? \d{4}\b', re.IGNORECASE)
    
#     # Function to replace the found date with its standardized format
#     def replace_with_standard_date(match):
#         try:
#             # Parse the date found by the regex
#             parsed_date = parse(match.group(0))
#             # Return the date in the standardized format YYYY-MM-DD
#             return parsed_date.strftime('%Y-%m-%d')
#         except ValueError:
#             # In case of a parsing error, return the original text
#             return match.group(0)
    
#     # Replace dates in the text with their standardized ISO 8601 format
#     standardized_text = date_pattern.sub(replace_with_standard_date, text)
    
#     return standardized_text

# def preprocess_text(text):
#     """
#     Preprocess a single document by standardizing dates, expanding abbreviations, tokenizing,
#     converting to lowercase, lemmatizing, removing stopwords, and punctuation.
#     """
#     # Standardize dates before expanding abbreviations
#     text_with_standard_dates = standardize_date(text)
#     expanded_text = expand_abbreviations(text_with_standard_dates, abbreviation_expansions)
#     doc = nlp(expanded_text)
#     return " ".join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)


def preprocess_text(text):
    """
    Preprocess a single document by expanding abbreviations, tokenizing, converting to lowercase,
    lemmatizing, removing stopwords, and punctuation.
    """
    expanded_text = expand_abbreviations(text, abbreviation_expansions)
    doc = nlp(expanded_text)
    return " ".join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)

def preprocess_texts_in_batches(texts, batch_size=256):
    """
    Expand abbreviations and process texts in batches, applying preprocessing steps.
    """
    processed_texts = []
    for doc in nlp.pipe([expand_abbreviations(text, abbreviation_expansions) for text in texts], batch_size=batch_size):
        processed_text = " ".join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)
        processed_texts.append(processed_text)
    return processed_texts

def get_texts_with_ids(df, text_type):
    """Get texts and their doc_ids based on type (title/description)."""
    relevant_df = df[df['type'] == text_type]
    return relevant_df['doc_id'].tolist(), relevant_df['value'].tolist()

def save_processed_data(doc_ids, processed_texts, output_file_path):
    """Save processed texts with their doc_ids to a CSV file."""
    processed_df = pd.DataFrame({'doc_id': doc_ids, 'value': processed_texts})
    processed_df.to_csv(output_file_path, sep='\t', index=False, header=None)

def main():
    file_path = 'data/raw_data/sample_data.csv'
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

    # Process and save titles
    title_ids, titles = get_texts_with_ids(df, 'title')
    processed_titles = preprocess_texts_in_batches(titles)  # No need to convert to list, it's already a list from get_texts_with_ids
    save_processed_data(title_ids, processed_titles, 'data/processed_data_title.csv')

    # Process and save descriptions
    description_ids, descriptions = get_texts_with_ids(df, 'description')
    processed_descriptions = preprocess_texts_in_batches(descriptions)
    save_processed_data(description_ids, processed_descriptions, 'data/processed_data_descr.csv')

if __name__ == '__main__':
    main()