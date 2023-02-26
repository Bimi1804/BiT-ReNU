# Test interface NL2DB
import os
import pandas as pd

from python_scripts.DB_module import *
from python_scripts.NLP_module import *
from python_scripts.NL_filter import *

db_mod = DB_Handler()
NLP_mod = NLP_Handler()

db_mod.create_new_project("test_req1")
db_mod.set_curr_project("test_req1")


with open(os.getcwd()+"\\test_cases\\test_requirements_NL.txt") as file:
	lines = file.readlines()
	lines_clean = []
	for l in lines:
		l = l.replace("\n","")
		lines_clean.append(l)

#--------------------------------------------------------
import spacy
import pandas as pd
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")

#test_line = nlp(lines_clean[10])

# Remove determiniter and punctuation:--------------------
lines_clean2 = []
for i in lines_clean:
	doc = nlp(i)
	line = []
	pos_line=[]
	for token in doc:
		if token.pos_ != "DET" and token.pos_ != "PUNCT":
			line.append(token)
		pos_line.append(token.pos_)
	lines_clean2.append(line)

################ FILTER ####################################################
# Filter attributes:--------------------------------------
lines_clean3 = []
lines_attr = []
for line in lines_clean2:
	for token in line:
		if token.lemma_ == "have":
			lines_attr.append(line)
			break
	else:
		lines_clean3.append(line)


# Filter generalization and composition:-----------------
lines_clean4 = []
lines_gen_and_comp = []
for line in lines_clean3:
	for token in line:
		if token.dep_ == "ROOT":
			if token.lemma_ == "be":
				lines_gen_and_comp.append(line)
				break
	else:
		lines_clean4.append(line)

lines_gen = []
lines_comp = []
for line in lines_gen_and_comp:
	for token in line:
		if token.tag_ == "IN":
			lines_comp.append(line)
			break
	else:
		lines_gen.append(line)

# Filter active/passive association:----------------------------------
lines_act = []
lines_pass = []
for line in lines_clean4:
	for token in line:
		if token.dep_ == "nsubjpass":
			lines_pass.append(line)
			break
	else:
		lines_act.append(line)














# Read DB
#for df in db_mod.read_all_db():
#	print(df)
#	print("")


NL_filter = NL_Filter()

output = NL_filter.filter_nl(lines_clean)




print("original:---------------------------")
for i in lines_clean:
	print(i)

print("\nAttributes:-----------------------")
for i in output[0]:
	print(i)

print("\nGeneralization:--------------------")
for i in output[1]:
	print(i)

print("\nComposition:-----------------------")
for i in output[2]:
	print(i)

print("\nActive Association:----------------")
for i in output[3]:
	print(i)

print("\nPassive Association:---------------")
for i in output[4]:
	print(i)
