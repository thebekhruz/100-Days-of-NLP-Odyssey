from transformers import pipeline
from dateutil.parser import parse

# Load the NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Sample text
text = "I have an appointment on the 13th of February, 2024."

# Perform named entity recognition to find dates
entities = ner_pipeline(text)

# Function to replace dates in the text with formatted date
def replace_dates(text, entities):
    for entity in entities:
        if entity['entity'] == 'B-DATE' or entity['entity'] == 'I-DATE':
            date_text = text[entity['start']:entity['end']]
            try:
                # Parse and format the date
                formatted_date = parse(date_text).strftime('%Y-%m-%d')
                text = text.replace(date_text, formatted_date)
            except ValueError:
                pass  # Skip if the date can't be parsed/formatted
    return text

# Replace dates in the text
formatted_text = replace_dates(text, entities)
print(formatted_text)
