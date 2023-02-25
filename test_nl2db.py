# Test interface NL2DB
import os
import pandas as pd

from python_scripts.DB_module import *
from python_scripts.NLP_module import *

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

#------------------------------------
import spacy
import pandas as pd
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")

test_line = nlp(lines_clean[10])

# Remove determiniter and punctuation:
lines_clean2 = []
for i in lines_clean:
	doc = nlp(i)
	line = []
	pos_line=[]
	for token in doc:
		if token.pos_ != "DET" and token.pos_ != "PUNCT":
			line.append(token)
		pos_line.append(token.pos_)
	#print(line)
	#print(pos_line)
	#print("")
	lines_clean2.append(line)

# Filter attributes:
lines_clean3 = []
lines_attr = []
for line in lines_clean2:
	for token in line:
		if token.lemma_ == "have":
			lines_attr.append(line)
			break
	else:
		lines_clean3.append(line)


# Filter generalization and composition:
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
	line_tok = []
	line_dep = []
	line_head_pos = []
	for token in line:
		line_tok.append(token)
		line_dep.append(token.dep_)
		line_head_pos.append(token.head.text)
	print(line_tok)
	print(line_dep)
	print(line_head_pos)
	print("")




# Filter active association:

# Filter passive association:

# Filter composition:







# Read DB
#for df in db_mod.read_all_db():
#	print(df)
#	print("")
