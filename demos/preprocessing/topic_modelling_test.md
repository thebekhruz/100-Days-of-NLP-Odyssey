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


