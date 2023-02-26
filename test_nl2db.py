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

#print("\nAttributes:-----------------------")
#for i in output[0]:
#	print(i)

#print("\nGeneralization:--------------------")
#for i in output[1]:
#	print(i)

#print("\nComposition:-----------------------")
#for i in output[2]:
#	print(i)

#print("\nActive Association:----------------")
#for i in output[3]:
#	print(i)

#print("\nPassive Association:---------------")
#for i in output[4]:
#	print(i)


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
for token in doc_no_punctdet:
	if token.dep_ == "compound":
		combination = token.text + token.head.text
		doc_nlp.append(combination)
print(doc_nlp)


