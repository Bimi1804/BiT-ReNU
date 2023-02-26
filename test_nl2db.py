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
import pandas as pd
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")

#test_line = nlp(lines_clean[10])



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
