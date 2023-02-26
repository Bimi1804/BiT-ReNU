# Test interface NL2DB
import os
import pandas as pd

from python_scripts.DB_module import *
from python_scripts.NL_module import *

db_mod = DB_Handler()

db_mod.create_new_project("test_req1")
db_mod.set_curr_project("test_req1")


with open(os.getcwd()+"\\test_cases\\test_requirements_NL.txt") as file:
	lines = file.readlines()
	lines_clean = []
	for l in lines:
		l = l.replace("\n","")
		lines_clean.append(l)

#--------------------------------------------------------
import pandas as pd
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")

#test_line = nlp(lines_clean[10])



# Read DB
#for df in db_mod.read_all_db():
#	print(df)
#	print("")


NL_filter = NL_Filter()
NL_SQL_transformer = NL_SQL_Transformer()
output = NL_filter.filter_nl(lines_clean)
#NL_SQL_transformer.attr_to_sql(output[0])


#print("original:---------------------------")
#for i in lines_clean:
#	print(i)
"""
print("\nAttributes:-----------------------")
for i in output[0]:
	line = []
	print(i)
	for token in i:
		line.append(token.dep_)
	print(line)
	print("")

print("\nGeneralization:--------------------")
for i in output[1]:
	line = []
	print(i)
	for token in i:
		line.append(token.dep_)
	print(line)
	print("")

print("\nComposition:-----------------------")
for i in output[2]:
	line = []
	print(i)
	for token in i:
		line.append(token.dep_)
	print(line)
	print("")

print("\nActive Association:----------------")
for i in output[3]:
	line = []
	print(i)
	for token in i:
		line.append(token.dep_)
	print(line)
	print("")

print("\nPassive Association:---------------")
for i in output[4]:
	line = []
	print(i)
	for token in i:
		line.append(token.dep_)
	print(line)
	print("")
"""

import spacy
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")


sentence = "Universtiy employees have a matriculation number."

doc = nlp(sentence)
doc_no_punctdet = []
for token in doc:
	if token.pos_ != "DET" and token.pos_ != "PUNCT":
		doc_no_punctdet.append(token)
print(doc_no_punctdet)


doc_nlp = []
nsubj_comp = []
dobj_comp = []
for token in doc_no_punctdet:
	if token.dep_ == "compound":
		if  "subj" in token.head.dep_:
			nsubj_comp.append(token)
			nsubj_comp.append(token.head)
		if "obj" in token.head.dep_:
			dobj_comp.append(token)
			dobj_comp.append(token.head)
		
	doc_nlp.append(token.head.dep_)

print(doc_nlp)
print(nsubj_comp)
print(dobj_comp)
subj = ""
for token in nsubj_comp:
	subj = subj + token.lemma_.lower()
print(subj)
obj = ""
for token in dobj_comp:
	obj = obj + token.lemma_.lower()
print(obj)

