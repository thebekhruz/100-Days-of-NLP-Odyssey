import dateparser

sentence = "Parade of the Royal Bucks Hussars on 11th of August 1914 up Queen Victoria Road,turning into the high Street watched by crowds"

# Attempt to parse any date from the given sentence
parsed_date = dateparser.parse(sentence)

if parsed_date:
    normalized_date = parsed_date.strftime('%Y-%m-%d')
    print(f"Extracted Date: {normalized_date}")
else:
    print("No date could be extracted.")
