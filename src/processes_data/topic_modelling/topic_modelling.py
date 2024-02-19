import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel, LdaModel
from gensim.models.phrases import Phrases
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import time


def build_ngram_models(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=256)
    trigram = gensim.models.Phrases(bigram[texts], threshold=256)
    return gensim.models.phrases.Phraser(bigram), gensim.models.phrases.Phraser(trigram)


def apply_ngrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def load_text_data(file_path, column_name='title'):
    try:
        df = pd.read_csv(file_path, delimiter='\t', header=None, names=[column_name])
        return df[column_name].astype(str).tolist()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def create_dictionary_corpus(texts):
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

def calculate_coherence_score(n, alpha, beta, corpus, id2word, texts):
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=n, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha=alpha,
                                           per_word_topics=True,
                                           eta=beta)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    return coherence_lda

def main():
    start_time = time.time()
    file_path = 'data/intermediate/preprocessing/combined_df_for_lda.csv'
    titles = load_text_data(file_path, 'title')
    
    processed_titles = [title.split() for title in titles]
    bigram_mod, trigram_mod = build_ngram_models(processed_titles)
    data_with_ngrams = apply_ngrams(processed_titles, bigram_mod, trigram_mod)
    
    id2word, corpus = create_dictionary_corpus(data_with_ngrams)

    # Hyperparameters
    no_of_topics = [14]
    alpha_list = ['symmetric',0.3,0.5,0.7]
    beta_list = ['auto',0.3,0.5,0.7]

    for n in no_of_topics:
        for alpha in alpha_list:
            for beta in beta_list:
                coherence_score = calculate_coherence_score(n, alpha, beta, corpus, id2word, data_with_ngrams)
                print(f"n: {n}; alpha: {alpha}; beta: {beta}; Coherence Score: {coherence_score}")

    # Example of building a single LDA model with the best parameters found
    # This section can be modified according to the best parameters identified
    lda_model = build_lda_model(corpus, id2word, num_topics=7)  # Example: num_topics=7

    # Calculate perplexity and coherence score for the selected model
    perplexity = lda_model.log_perplexity(corpus)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_with_ngrams, dictionary=id2word, coherence='c_v')
    print(f'\nPerplexity: {perplexity}')
    print('Coherence Score:', coherence_model_lda.get_coherence())

    # Visualize the topics
    vis = gensimvis.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'lda_visualization.html')

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()


