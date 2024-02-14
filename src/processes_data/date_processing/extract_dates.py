"""
The following file is used to preprocess data. This includes expanding abbreviations, tokenizing, converting to lowercase,
    lemmatizing, removing stopwords, and punctuation.


    TODO:
    [] -> Make the dates into ISO FORM - YYYY-MM-DD
"""

import time
import pandas as pd
import spacy
import re
from dateutil.parser import parse
from datetime import datetime

century_mappings = {
    "20th century": ("1900-01-01", "1999-12-31"),
    "beginning of the 20th century": ("1900-01-01", "1919-12-31"),
    "early 20th century": ("1900-01-01", "1939-12-31"),
    "mid 20th century": ("1940-01-01", "1969-12-31"),
    "late 20th century": ("1970-01-01", "1999-12-31"),
    "19th century": ("1800-01-01", "1899-12-31"),
    "beginning of the 19th century": ("1800-01-01", "1819-12-31"),
    "early 19th century": ("1800-01-01", "1839-12-31"),
    "mid 19th century": ("1840-01-01", "1869-12-31"),
    "late 19th century": ("1870-01-01", "1899-12-31"),
    "18th century": ("1700-01-01", "1799-12-31"),
    "beginning of the 18th century": ("1700-01-01", "1719-12-31"),
    "early 18th century": ("1700-01-01", "1739-12-31"),
    "mid 18th century": ("1740-01-01", "1769-12-31"),
    "late 18th century": ("1770-01-01", "1799-12-31"),
    "17th century": ("1600-01-01", "1699-12-31"),
    "beginning of the 17th century": ("1600-01-01", "1619-12-31"),
    "early 17th century": ("1600-01-01", "1639-12-31"),
    "mid 17th century": ("1640-01-01", "1669-12-31"),
    "late 17th century": ("1670-01-01", "1699-12-31"),
    "16th century": ("1500-01-01", "1599-12-31"),
    "beginning of the 16th century": ("1500-01-01", "1519-12-31"),
    "early 16th century": ("1500-01-01", "1539-12-31"),
    "mid 16th century": ("1540-01-01", "1569-12-31"),
    "late 16th century": ("1570-01-01", "1599-12-31"),
    # You can continue to add more for earlier centuries if needed
}

# Corrected Abbreviations map
ABBREVIATION_EXPANSIONS = {
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
    "Apr.": "April ", "Apr ": "April",
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

# Precompile regular expressions for efficiency
# APOSTROPHE_PATTERN = re.compile(r"[^\w\d\s]+")
# APOSTROPHE_PATTERN = re.compile(r"(\d’s)|[^\w\s]+")
NUMERICAL_S_PATTERN = re.compile(r"\b(\d+)s\b", re.IGNORECASE)
POSSESSIVE_PATTERN = re.compile(r"\b(?:’s|'s)\b", re.IGNORECASE)
BRACKET_PATTERN = re.compile(r"\[|\]")


# Load the SpaCy model with specific components disabled for efficiency
NLP = spacy.load("en_core_web_md") # NER enabled for date normalization


def expand_abbreviations(text):
    """Replace abbreviations in the text with their expanded forms."""
    for abbr, expansion in ABBREVIATION_EXPANSIONS.items():
        pattern = r'\b' + re.escape(abbr) + r'\b(?![\'’])'
        text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
    return text

def remove_embedded_brackets(text):
    """Remove inner brackets found within words."""
    return BRACKET_PATTERN.sub(" ", text)



def remove_apostrophies(text):
    """Remove possessive 's or ’s from words and trailing 's' from numbers, handling different apostrophes and ensuring word boundary."""
    # Remove possessive 's or ’s
    text = POSSESSIVE_PATTERN.sub("", text)
    return text


def remove_trailing_s(text):
    # Remove trailing 's' from numbers (e.g., 1980s -> 1980)
    text = NUMERICAL_S_PATTERN.sub(r"\1", text)
    return text



def normalize_and_replace_dates(text):
    doc = NLP(text)  # Process text with spaCy

    modified_text = text

    # Find dates using NER
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            original_date = ent.text
            date_replaced = False
            
            # Check against century mappings first
            for desc, (start, end) in century_mappings.items():
                try:
                    if desc in original_date:
                        modified_text = modified_text.replace(original_date, start)  # Use start of range
                        date_replaced = True
                        break
                except ValueError:
                        # print(f"Could not parse date: {original_date}")
                    continue

            # Special handling for "mid YYYY"
            if 'mid' in original_date.lower():
                try:
                    year = re.search(r'\d{4}', original_date).group(0)
                    normalized_date = f"{year}-06-15"
                    modified_text = modified_text.replace(original_date, normalized_date)
                    date_replaced = True
                except AttributeError:
                    print(f"Could not find year in: {original_date}")
            
            # Handling approximate dates like "1956/1957"
            if not date_replaced and '/' in original_date:
                try:
                    first_year = original_date.split('/')[0]
                    if first_year.isdigit():
                        normalized_date = f"{first_year}-01-01"  # Using Jan 1 as a default date
                        modified_text = modified_text.replace(original_date, normalized_date)
                        date_replaced = True
                except (IndexError, ValueError):
                    print(f"Could not normalize approximate date: {original_date}")

            # Handling date ranges like "1926-1928" or "1926-28"
            if not date_replaced and '-' in original_date:
                try:
                    # Extract the first year from the range
                    first_year = original_date.split('-')[0]
                    if first_year.isdigit():
                        normalized_date = f"{first_year}-01-01"  # Using Jan 1 as a default date
                        modified_text = modified_text.replace(original_date, normalized_date)
                        date_replaced = True
                except (IndexError, ValueError):
                    print(f"Could not normalize date range: {original_date}")

            # If not replaced by any specific handling, attempt parsing with enhanced flexibility
            if not date_replaced:
                try:
                    normalized_date = parse(original_date, default=datetime(1800, 1, 1), fuzzy=True).strftime('%Y-%m-%d')
                    modified_text = modified_text.replace(original_date, normalized_date)
                except ValueError:
                    # print(f"Could not parse date: {original_date}")
                    continue

    return modified_text




def preprocess_texts_in_batches(texts, batch_size=256):
    """Process texts in batches with preprocessing steps."""
    preprocessed_texts = [
        remove_embedded_brackets(
            expand_abbreviations(
                normalize_and_replace_dates(
                    remove_trailing_s(
                     remove_apostrophies(text if isinstance(text, str) else "[ No Description Available ]")))))

        for text in texts
    ]
    # date_formatted_texts = [format_dates_with_ner(text) for text in preprocessed_texts]
    
    processed_texts = []
    for doc in NLP.pipe(preprocessed_texts, batch_size=batch_size, disable=["ner"]):  # Disable NER here as it's already applied
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
    """Main function to orchestrate the preprocessing pipeline."""
    start_time = time.time()

    # Define file paths
    # input_file_path = 'data/raw_data/swop_triples.csv'
    input_file_path = 'data/raw_data/partitions/partition_2500ent.csv'
    output_file_path_titles = 'data/processed_data/processed_data_title_test_dates.csv'
    output_file_path_descriptions = 'data/processed_data/processed_data_descr.csv'

    # Load data
    df = pd.read_csv(input_file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

    # Process and save titles
    title_ids, titles = get_texts_with_ids(df, 'title')
    processed_titles = preprocess_texts_in_batches(titles)

    save_processed_data(title_ids, processed_titles, output_file_path_titles, 'title')

    # Process and save descriptions
    description_ids, descriptions = get_texts_with_ids(df, 'description')
    processed_descriptions = preprocess_texts_in_batches(descriptions)
    save_processed_data(description_ids, processed_descriptions, output_file_path_descriptions, 'description')
    
    end_time = time.time()
    print(f"\nSuccess! \nExecution Time: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()