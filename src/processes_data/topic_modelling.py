import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel

import pandas as pd

# spacy is not used in the revised code since preprocessing is assumed to be done
# import spacy

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

import time

# Functions for building bigram and trigram models are kept as they might be useful for phrase detection in titles
def build_bigram_trigram_models(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[texts], threshold=100)
    return gensim.models.phrases.Phraser(bigram), gensim.models.phrases.Phraser(trigram)

def apply_bigram_trigram(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def load_titles(file_path):
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['title'])
    # Convert all titles to strings to avoid AttributeError
    titles = df['title'].astype(str).tolist()
    return titles


def load_desciptions(file_path):
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=['description'])
    # Convert all titles to strings to avoid AttributeError
    titles = df['description'].astype(str).tolist()
    return titles

def create_dictionary_and_corpus(texts):
    id2word = corpora.Dictionary(texts)
    id2word.filter_extremes(no_below=5, no_above=0.5)
    corpus = [id2word.doc2bow(text, allow_update=True) for text in texts]
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
    start_time = time.time()

    # file_path = 'data/processed_data/processed_data_title.csv'
    # titles = load_titles(file_path)

    file_path = 'data/processed_data/processed_data_descr.csv'
    titles = load_desciptions(file_path)
    
    # Ensure titles are strings and split them into lists of words
    processed_titles = [title.split() for title in titles]
    bigram_mod, trigram_mod = build_bigram_trigram_models(processed_titles)
    data_with_bigrams_trigrams = apply_bigram_trigram(processed_titles, bigram_mod, trigram_mod)
    
    id2word, corpus = create_dictionary_and_corpus(data_with_bigrams_trigrams)
    lda_model = build_lda_model(corpus=corpus, dictionary=id2word, num_topics=5)

    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_with_bigrams_trigrams, dictionary=id2word, coherence='c_v')
    print('\nCoherence Score: ', coherence_model_lda.get_coherence())

    vis = gensimvis.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'lda_visualization_desc.html')

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()



