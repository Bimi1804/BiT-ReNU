# NLP Module for BiT-Renu

# Testing the spaCy tool


# Libraries:

import spacy

import en_core_web_sm
nlp = en_core_web_sm.load()



# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")




#----------------------------
test_sentence = "The user has a name."

doc = nlp(test_sentence)


for token in doc:
    # Get the token text, part-of-speech tag and dependency label
    token_text = token.text
    token_lemma = token.lemma_
    token_pos = token.pos_
    token_tag = token.tag_
    token_dep = token.dep_
    # This is for formatting only
    print(f"{token_text:<12}{token_lemma:<10}{token_pos:<10}{token_tag:<10}{token_dep:<10}")

