import time
import pandas as pd
import spacy
import re
from dateutil.parser import parse

# Load the SpaCy model with specific components disabled for efficiency
NLP = spacy.load("en_core_web_md", disable=["ner", "parser"])


# Corrected Abbreviations map
ABBREVIATION_EXPANSIONS = {
    # Geographical:
    "PH": "Public house",
    "R.Wye": "River Wye",
    "HW": "High Wycombe",
    "HQ": "Headquarters",
    "HDC": "High Wycombe District Council",
    # Historical and Military:
    "W.R.A.F.": "Women's Royal Air Force.",
    "V.E.Day": "Victory in Europe Day", 'VE Day': "Victory in Europe Day",
    "WWI": "First World War",
    "WWII": "Second World War",
    "RAF": "Royal Air Force",
    "HMS": "Her Majesty's Ship",
    "HRH": "His Royal Highness",
    "MP": "Member of Parliament",
    "BFP": "Bucks Free Press",
    "VJ Day": "Victory over Japan Day", "VJ-day": "Victory over Japan Day",
    # Compass directions
    "N": "North",
    "S": "South",
    "E": "East",
    "W": "West",
    "NE": "Northeast",
    "NW": "Northwest",
    "SE": "Southeast",
    "SW": "Southwest",
    "NNE": "North-Northeast",
    "ENE": "East-Northeast",
    "ESE": "East-Southeast",
    "SSE": "South-Southeast",
    "SSW": "South-Southwest",
    "WSW": "West-Southwest",
    "WNW": "West-Northwest",
    "NNW": "North-Northwest",
    # Street Names
    "St": "Street",
    "Rd": "Road",
    "Ave": "Avenue",
    "Dr": "Drive",
    "Ln": "Lane",
    "Ct": "Court",
    "Sq": "Square",
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
    "Dec.": "December ", "Dec": "December",
    # Other
    "FC": "Football Club"

    # Extend this list as needed
}

def expand_abbreviations(text):
    """Replace abbreviations in the text with their expanded forms."""
    for abbr, expansion in ABBREVIATION_EXPANSIONS.items():
        pattern = r'\b' + re.escape(abbr) + r'\b(?![\'’])'
        text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
    return text

# Precompile regular expressions for efficiency
APOSTROPHE_PATTERN = re.compile(r"[^\w\d\s]+")
BRACKET_PATTERN = re.compile(r"\[|\]")
NUMBER_WITH_S_PATTERN = re.compile(r"\b(\d+)s\b")

def clean_text(text):
    """Clean a single text string by removing apostrophes and brackets."""
    text = APOSTROPHE_PATTERN.sub("", text)
    text = NUMBER_WITH_S_PATTERN.sub("\1", text) 
    text = BRACKET_PATTERN.sub(" ", text)
    return text


def preprocess_texts_in_batches(texts, batch_size=256):
    """Process texts in batches with preprocessing steps."""
    preprocessed_texts = [
        expand_abbreviations(clean_text(text if isinstance(text, str) else "[ No Description Available ]"))
        for text in texts
    ]

    processed_texts = []
    for doc in NLP.pipe(preprocessed_texts, batch_size=batch_size):  # Disable NER here as it's already applied
        processed_text = " ".join(token.text.lower() for token in doc if not token.is_stop and not token.is_punct)
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
    input_file_path = 'data/intermediate/swop_triples_cleaned.csv'
    output_file_path_titles = 'data/intermediate/preprocessing/processed_data_title_no_lemma.csv'
    output_file_path_descriptions = 'data/intermediate/preprocessing/processed_data_descr_no_lemma.csv'

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