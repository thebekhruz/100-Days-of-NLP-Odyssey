import re
from dateutil.parser import parse

# Sample texts
sentence = "Parade of the Royal Bucks Hussars on 11th of August 1914 up Queen Victoria Road,turning into the high Street watched by crowds"


# Regex patterns to identify dates
date_patterns = [
    r"\d{1,2}(st|nd|rd|th)?\s\w+\s\d{4}",  # Matches "7th July 1893", "11th August 1914"
    r"\d{4}"  # Matches "1950", "1947"
]

# Function to normalize date
def normalize_date(text):
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(0)
            # Trying to parse date
            try:
                date = parse(date_str, fuzzy=True)
                # Returning formatted date
                return date.strftime("%Y-%m-%d")
            except ValueError:
                # Handling dates that cannot be directly parsed
                # For example, "about 1950" might be defaulted to "1950-01-01"
                if re.match(r"\d{4}", date_str):
                    return f"{date_str}-01-01"
    return "Unknown Date Format"

# Applying normalization
normalized_date = normalize_date(sentence)
print(normalized_date)
