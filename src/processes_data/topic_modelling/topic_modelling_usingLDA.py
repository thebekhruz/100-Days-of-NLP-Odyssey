import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel, LdaModel
from gensim.models.phrases import Phrases
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import time
import spacy



# Load the spaCy language model
nlp = spacy.load("en_core_web_md")

# Define your custom stopwords list
custom_stopwords = ['nort', 'east', 'south', 'west',
                    'northeast', 'northwest', 'southeast', 'southwest',
                    'looking', 'view', 'wycombe', 'street', 'high']

# Update the spaCy stopwords list with your custom stopwords
nlp.Defaults.stop_words.update(custom_stopwords)

# Function to remove stopwords
def remove_custom_stopwords(doc):
    return [token.text for token in nlp(doc) if token.text not in nlp.Defaults.stop_words]

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



def build_lda_model(corpus, dictionary, num_topics=7):
    # Best hyperparameters:
    # n: 5; alpha: 0.7; beta: 0.3; Coherence Score: 0.5538250235146185
    # n: 7; alpha: 0.7; beta: 0.5; Coherence Score: 0.5230671297664795
    return LdaModel(corpus=corpus,
                        id2word=dictionary,
                        num_topics=num_topics, 
                        random_state=100,
                        update_every=1,
                        chunksize=100,
                        passes=10,
                        alpha=0.7,
                        per_word_topics=True,
                        eta=0.3)


def main():
    start_time = time.time()

    file_path = 'data/intermediate/preprocessing/combined_df_for_lda.csv'
    # file_path = 'data/intermediate/preprocessing/processed_data_title.csv'
    titles = load_text_data(file_path, 'title')
    

    processed_titles = [remove_custom_stopwords(title) for title in titles]
    bigram_mod, trigram_mod = build_ngram_models(processed_titles)
    data_with_ngrams = apply_ngrams(processed_titles, bigram_mod, trigram_mod)
    
    id2word, corpus = create_dictionary_corpus(data_with_ngrams)
    lda_model = build_lda_model(corpus, id2word, num_topics=5)


    # processed_titles = [title.split() for title in titles]
    # bigram_mod, trigram_mod = build_ngram_models(processed_titles)
    # data_with_ngrams = apply_ngrams(processed_titles, bigram_mod, trigram_mod)
    
    # id2word, corpus = create_dictionary_corpus(data_with_ngrams)
    # lda_model = build_lda_model(corpus, id2word, num_topics=5)

    # Extract topics
    top_topics = lda_model.show_topics(num_topics=50, num_words=10, formatted=False)
    CATEGORIES = [{f"Topic {topic_id}": [word for word, _ in words]} for topic_id, words in top_topics]


    # Calculate perplexity and coherence score
    perplexity = lda_model.log_perplexity(corpus)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_with_ngrams, dictionary=id2word, coherence='c_v')

    print(CATEGORIES)
    print(f'\nPerplexity: {perplexity}')
    print('Coherence Score:', coherence_model_lda.get_coherence())

    # # Visualize the topics
    vis = gensimvis.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'docs/visualisations/lda_visualization_combined_texts.html')

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()


