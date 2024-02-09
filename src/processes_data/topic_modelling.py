# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pandas as pd

# spacy for lemmatization
import spacy
nlp = spacy.load("en_core_web_lg")

def preprocess_text(text):
    return " ".join(token.lemma_ for token in nlp(text.lower()) if not token.is_stop and not token.is_punct)

# Build the bigram and trigram models
def build_bigram_trigram_models(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[texts], threshold=100)  
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    return bigram_mod, trigram_mod


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def get_texts_and_ids(df):
    # Return both 'doc_id' and 'value' for filtering
    filtered = df[df['type'].isin(['title', 'description'])][['doc_id', 'value']]
    return filtered


def main():

    file_path = 'data/raw_data/sample_data.csv'
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])

    
    texts =get_texts_and_ids(df)
    processed_text = texts['value'].apply(preprocess_text)
    bigram_mod, trigram_mod = build_bigram_trigram_models(processed_text)

    # Form Bigrams
    data_words_bigrams = make_bigrams(processed_text, bigram_mod)
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])


    print(data_lemmatized[:1])


    # return bigram_mod, trigram_mod

biagram, _ = main()
# print(biagram[:1])
