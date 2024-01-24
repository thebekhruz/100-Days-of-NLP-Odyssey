import spacy
from spacy.symbols import ORTH, LEMMA


# Tokenisation
nlp = spacy.load('en_core_web_sm')
doc = nlp(u'I am studying at UoM')
def tokenise(input_data):
    tokens = [token.text for token in input_data]
    return tokens


def lemmatise(input_data, flag=False):
    lemmas = []
    for token in input_data:
        # If the special flag is set and the token text is 'UoM'
        if flag and token.text == 'UoM':
            lemmas.append('University of Manchester')
        else:
            lemmas.append(token.lemma_)
    return lemmas


def pos_tagging(input_data):
    pos_tags = [(token.text, token.pos_) for token in input_data]
    return pos_tags


def pipeline():
    tokens = tokenise(doc)
    print(tokens)

    lemmas = lemmatise(doc)
    print(lemmas)

    special_lemmas = lemmatise(doc, flag=True)
    print(special_lemmas)

    pos_taggers = pos_tagging(doc)
    print(pos_taggers)


pipeline()
    


# Lemmatisation

