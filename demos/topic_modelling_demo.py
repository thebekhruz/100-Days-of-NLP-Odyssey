"""
Topic Modeling Script Overview:
* Loads descriptions from a CSV file for topic modeling.
* Preprocesses text by applying bigram and trigram models for enhanced phrase detection.
* Generates a dictionary and corpus from the preprocessed text.
* Constructs an LDA model using Gensim to identify latent topics within the dataset.
* Calculates and prints the coherence score to evaluate model quality.
* Visualizes topics with pyLDAvis and saves the output as an HTML file.
Purpose: To uncover and visualize latent thematic structures in text data.

Experiments:
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=50)
    trigram = gensim.models.Phrases(bigram[texts], threshold=50)
    Coherence Score:  0.40773674345906247
    ________________________________________________________________


    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[texts], threshold=100)
    Perplexity:  -8.019823279574403
    Coherence Score:  0.4912259518860383
    ________________________________________________________________


    bigram = gensim.models.Phrases(texts, min_count=5, threshold=150)
    trigram = gensim.models.Phrases(bigram[texts], threshold=150)
    Perplexity:  -8.015174480313167
    Coherence Score:  0.4748514002626062
    ________________________________________________________________

    bigram = gensim.models.Phrases(texts, min_count=5, threshold=200)
    trigram = gensim.models.Phrases(bigram[texts], threshold=200)
    Perplexity:  -7.928899988047125
    Coherence Score:  0.5238894711998521    
    ________________________________________________________________ 

    ***
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=256)
    trigram = gensim.models.Phrases(bigram[texts], threshold=256)
    Perplexity:  -7.913010402330108
    Coherence Score:  0.5374995385660457
    ***

    ________________________________________________________________
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=300)
    trigram = gensim.models.Phrases(bigram[texts], threshold=300)
    Perplexity:  -7.913490664575796
    Coherence Score:  0.43625522609244777
    ________________________________________________________________

    
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=350)
    trigram = gensim.models.Phrases(bigram[texts], threshold=350)
    Perplexity:  -7.823093867130277
    Coherence Score:  0.5237703615268858
    ________________________________________________________________


    bigram = gensim.models.Phrases(texts, min_count=5, threshold=450)
    trigram = gensim.models.Phrases(bigram[texts], threshold=450)
    Perplexity:  -7.865856236276151
    Coherence Score:  0.4938879780336124
    ________________________________________________________________


    bigram = gensim.models.Phrases(texts, min_count=5, threshold=450)
    trigram = gensim.models.Phrases(bigram[texts], threshold=450)
    ________________________________________________________________


"""



import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import time

# Functions for building bigram and trigram models are kept as they might be useful for phrase detection in titles
def build_bigram_trigram_models(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=256)
    trigram = gensim.models.Phrases(bigram[texts], threshold=256)
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


def build_lda_model(corpus, dictionary, num_topics=5):
    return LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=num_topics,
                         random_state=100,
                         update_every=1,
                         chunksize=1000,
                         passes=10,
                         alpha='auto',
                         per_word_topics=True)
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel, LdaModel
import pandas as pd
import matplotlib.pyplot as plt

# Assuming your preprocessing functions remain the same...

def evaluate_lda_model(corpus, dictionary, texts, alpha, eta):
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, random_state=100, update_every=1, chunksize=100, passes=10, alpha=alpha, eta=eta, per_word_topics=True)
    perplexity = lda_model.log_perplexity(corpus)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence = coherence_model_lda.get_coherence()
    return perplexity, coherence

def main():
    # Load your data and preprocess it
    file_path = 'data/processed_data/processed_data_descr.csv'
    descriptions = load_desciptions(file_path)
    processed_texts = [description.split() for description in descriptions]
    bigram_mod, trigram_mod = build_bigram_trigram_models(processed_texts)
    texts_with_bigrams_trigrams = apply_bigram_trigram(processed_texts, bigram_mod, trigram_mod)
    dictionary, corpus = create_dictionary_and_corpus(texts_with_bigrams_trigrams)

    # Define the range of hyperparameters to test
    alpha_values = ['symmetric', 'asymmetric', 'auto']
    eta_values = ['symmetric', 'auto']
    results = {'alpha': [], 'eta': [], 'perplexity': [], 'coherence': []}

    for alpha in alpha_values:
        for eta in eta_values:
            perplexity, coherence = evaluate_lda_model(corpus, dictionary, texts_with_bigrams_trigrams, alpha, eta)
            results['alpha'].append(alpha)
            results['eta'].append(eta)
            results['perplexity'].append(perplexity)
            results['coherence'].append(coherence)
            print(f"Alpha: {alpha}, Eta: {eta}, Perplexity: {perplexity}, Coherence: {coherence}")

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    
    # Perplexity Plot
    for eta in eta_values:
        idx = [i for i, x in enumerate(results['eta']) if x == eta]
        axs[0].plot([results['alpha'][i] for i in idx], [results['perplexity'][i] for i in idx], label=f'eta={eta}')
    axs[0].set_title('Perplexity by Alpha and Eta')
    axs[0].set_xlabel('Alpha')
    axs[0].set_ylabel('Perplexity')
    axs[0].legend()
    
    # Coherence Plot
    for eta in eta_values:
        idx = [i for i, x in enumerate(results['eta']) if x == eta]
        axs[1].plot([results['alpha'][i] for i in idx], [results['coherence'][i] for i in idx], label=f'eta={eta}')
    axs[1].set_title('Coherence by Alpha and Eta')
    axs[1].set_xlabel('Alpha')
    axs[1].set_ylabel('Coherence')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()




