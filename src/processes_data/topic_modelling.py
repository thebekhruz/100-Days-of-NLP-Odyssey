# Gensim
import gensim
import gensim.corpora as corpora
# from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
# from gensim.corpora import Dictionary

import numpy as np
import pandas as pd
from pprint import pprint

# spacy
import spacy
nlp = spacy.load("en_core_web_md", disable=["ner", "parser"])

# Visualisation
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import matplotlib.pyplot as plt


import time


def preprocess_texts(texts):
    """ Batch process a list of texts, applying preprocessing steps such as lemmatization and stopword removal."""
    processed_texts = []
    texts = [str(text) for text in texts]
    for doc in nlp.pipe(texts, batch_size=256):
        processed_texts.append([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    return processed_texts



# Build the bigram and trigram models
def build_bigram_trigram_models(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100)   # Higher threshold, fewer phrases.
    trigram = gensim.models.Phrases(bigram[texts], threshold=100)       # Higher threshold, fewer phrases.
    return gensim.models.phrases.Phraser(bigram), gensim.models.phrases.Phraser(trigram)


def apply_bigram_trigram(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc.split()] for doc in texts]


def make_trigrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc.split()]] for doc in texts]


def get_texts(df):
    return df[df['type'].isin(['title', 'description'])]['value'].tolist()

def create_dictionary_and_corpus(texts):
    id2word = corpora.Dictionary(texts)
    id2word.filter_extremes(no_below=5, no_above=0.5)                      # Remove extremely rare and common tokens
    corpus = [id2word.doc2bow(text, allow_update=True) for text in texts]  # Efficiently update dictionary
    return id2word, corpus


def build_lda_model(corpus, dictionary, num_topics=30):
    return LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=num_topics,
                         random_state=100,
                         update_every=1,
                         chunksize=1000,
                         passes=10,
                         alpha='auto',
                         per_word_topics=True)



def main():
    start_time = time.time()  # Start time measurement

    # file_path = 'data/raw_data/chunk/partition_2500ent.csv'
    file_path = 'data/raw_data/swop_triples.csv'
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])
    texts = get_texts(df)
    

    processed_texts = preprocess_texts(texts)
    bigram_mod, trigram_mod = build_bigram_trigram_models(processed_texts)
    data_with_bigrams_trigrams = apply_bigram_trigram(processed_texts, bigram_mod, trigram_mod)

    
    id2word, corpus = create_dictionary_and_corpus(data_with_bigrams_trigrams)
    lda_model = build_lda_model(corpus = corpus, dictionary =id2word, num_topics = 11)

    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_with_bigrams_trigrams, dictionary=id2word, coherence='c_v')
    print('\nCoherence Score: ', coherence_model_lda.get_coherence())

    # Visualisation of the LDA model
    vis = gensimvis.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'lda_visualization1.html')


    end_time = time.time()  # End time measurement
    print(f"Execution Time: {end_time - start_time} seconds")  # Print execution time 



# Only used to find optimal number of topics, never later. 
def find_optimal_k(limit=21, start=5, step=3):
    file_path = 'data/raw_data/swop_triples.csv'
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])
    texts = get_texts(df)

    processed_texts = preprocess_texts(texts)
    bigram_mod, trigram_mod = build_bigram_trigram_models(processed_texts)
    data_with_bigrams_trigrams = apply_bigram_trigram(processed_texts, bigram_mod, trigram_mod)

    id2word, corpus = create_dictionary_and_corpus(data_with_bigrams_trigrams)

    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaModel(corpus=corpus,
                         id2word=id2word,
                         num_topics=num_topics,
                         random_state=100,
                         update_every=1,
                         chunksize=100,
                         passes=10,
                         alpha='auto',
                         per_word_topics=True)

        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=data_with_bigrams_trigrams, dictionary=id2word, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    plt.plot(range(start, limit, step), coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()

    optimal_num_topics = range(start, limit, step)[coherence_values.index(max(coherence_values))]
    print("Optimal number of topics:", optimal_num_topics)

# Corrected function call with the right parameters

if __name__ == "__main__":

    find_optimal_k(limit=30, start=2, step=2) # Uncomment to find optimal number of topics
    # Optimum number of topics is 11.
    # main()
