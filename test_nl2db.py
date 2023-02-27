# Test interface NL2DB
import os
import pandas as pd

from python_scripts.DB_module import *
from python_scripts.NL_module import *

db_mod = DB_Handler()
NL_filter = NL_Filter()
NL_SQL_transformer = NL_SQL_Transformer()

db_mod.create_new_project("test_req1")
db_mod.set_curr_project("test_req1")


with open(os.getcwd()+"\\test_cases\\test_requirements_NL.txt") as file:
	lines = file.readlines()
	lines_clean = []
	for l in lines:
		l = l.replace("\n","")
		lines_clean.append(l)

#--------------------------------------------------------
output = NL_filter.filter_nl(lines_clean)
lines_attr = output[0]
lines_gen = output[1]
lines_comp = output[2]
lines_act = output[3]
lines_pass = output[4]

sql_queue = NL_SQL_transformer.transform_nl_sql(lines_attr,lines_gen,lines_comp,lines_act,lines_pass)
db_mod.write_to_db(sql_queue)


#Read DB
dataframes = db_mod.read_all_db()
print("Classes:-------------------")
#print(dataframes[0])
print("\nAttrbutes:-------------------")
#print(dataframes[1])
print("\nOperations:-------------------")
#print(dataframes[2])
print("\nAssociations:-------------------")
#print(dataframes[3].iloc[:,[0,2,4,5,6,7]])

# ----- Test Clean-up-------#
db_mod.delete_db_file("test_req1")

import re
for index, row in dataframes[1].iterrows():
	subj =""
	obj = ""
	if row[1].isupper() is True:
		subj = row[1]
	if row[1].isupper() is False:
		up_count = sum(1 for letter in row[1] if letter.isupper())
		if up_count < 2:
			subj = row[1].lower()
		if up_count > 1:
			subj_parts = re.findall('[A-Z][^A-Z]*',row[1])
			for word in subj_parts:
				if subj == "":
					subj = word.lower()
				elif subj != "":
					subj = f"{subj} {word.lower()}"
	if row[0].isupper() is True:
		obj = row[0]
	if row[0].isupper() is False:
		up_count = sum(1 for letter in row[0] if letter.isupper()) 
		if up_count == 0:
			obj = row[0]
		upper_ind = []
		for index in range(len(row[0])):
			if row[0][index].isupper() is True:
				upper_ind.append(index)
		if upper_ind != []:
			for i in range(len(upper_ind)):
				if i == 0:
					obj = row[0][0:upper_ind[i]].lower()
				if i < len(upper_ind)-1:
					obj = f"{obj} {row[0][upper_ind[i]:upper_ind[i]+1].lower()}"
				if i == len(upper_ind)-1:
					obj = f"{obj} {row[0][upper_ind[i]:].lower()}"
	subj_det = ""
	obj_det = ""
	vowels = ["a","e","i","o","u"]
	print(f"A {subj} has a {obj}.")
	print("")





