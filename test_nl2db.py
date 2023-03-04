# Test interface NL2DB
import os
import pandas as pd

from python_scripts.DB_module import *
from python_scripts.NL_module import *

db_mod = DB_Handler()
NL_filter = NL_Filter()
NL_SQL_transformer = NL_SQL_Transformer()
SQL_NL_morph = SQL_NL_Transformer()

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
#db_mod.delete_db_file("test_req1")

counter = 1
for i in SQL_NL_morph.attr_to_nl(dataframes[1]):
	print(f"{counter}: {i}")
	counter = counter +1

gen_sent, comp_sent, asc_sent = SQL_NL_morph.asc_to_nl(dataframes[3])
for i in gen_sent:
	print(f"{counter}: {i}")
	counter = counter +1
for i in comp_sent:
	print(f"{counter}: {i}")
	counter = counter +1
for i in asc_sent:
	print(f"{counter}: {i[0]}")
	counter = counter +1
	print(f"{counter}: {i[1]}")
	counter = counter +1
