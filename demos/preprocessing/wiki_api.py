import requests
import re

# Function to extract linked entities for semantic annotation
def extract_linked_entities(summary):
    linked_entities = re.findall(r'\[\[(.*?)\]\]', summary)
    return linked_entities


def fetch_wikipedia_summary(wikidata_id):
    # Fetch Wikipedia title from Wikidata
    wikidata_response = requests.get(
        "https://www.wikidata.org/w/api.php",
        params={
            "action": "wbgetentities",
            "ids": wikidata_id,
            "format": "json",
            "props": "sitelinks/urls"
        }
    )
    wikidata_data = wikidata_response.json()
    wikipedia_title = wikidata_data["entities"][wikidata_id]["sitelinks"]["enwiki"]["title"]
    
    # Fetch summary from Wikipedia
    wikipedia_response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "titles": wikipedia_title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
        }
    )
    wikipedia_data = wikipedia_response.json()
    page_id = next(iter(wikipedia_data["query"]["pages"]))
    summary = wikipedia_data["query"]["pages"][page_id]["extract"]
    
    return summary

# Example usage
wikidata_id = "Q64116"
summary = fetch_wikipedia_summary(wikidata_id)
linked_entities = extract_linked_entities(summary)
print('\n' + summary+ '\n')

print(linked_entities)
