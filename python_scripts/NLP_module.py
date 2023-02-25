# NLP Module for BiT-Renu

# Libraries:
import spacy
import pandas as pd
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")

class NLP_Handler:
	"""Manages NLP tasks"""

	def __init__(self, nlp=nlp):
		self.nlp = nlp


	def tokenize(self,sent_list):
		tok_sent_list = []
		for sentence in sent_list:
			sent_tokens = nlp(sentence)
			for token in sent_tokens:
				tok_sent_list.append(token.text)
		return tok_sent_list

	def lemmatize(self,sent_list):
		pass

	def type_dependency(self,sent_list):
		pass



	def pos_tagger():
		pass



		







#----------Tests----------

def test_NLP():
	test_sentence = "The user has a report."
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

def test_2():
	NLP_mod = NLP_Handler(nlp)

	req = ["The user creates a report."]
	for i in NLP_mod.tokenize(req):
		print(i)

#test_2()
