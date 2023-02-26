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
sql_attr = NL_SQL_transformer.attr_to_sql(lines_attr)
db_mod.write_to_db(sql_attr)



#Read DB
for df in db_mod.read_all_db():
	print(df)
	print("")


for i in lines_gen:
	print(i)




# ----- Test Clean-up-------#
db_mod.delete_db_file("test_req1")




