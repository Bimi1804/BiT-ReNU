# Evaluation Tests:
import os
script_path = os.path.abspath(__file__)
folder = os.path.dirname(script_path)
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)



# Setup:
from python_scripts.DB_module import *
from python_scripts.NL_module import *
from python_scripts.UML_module import *

# DB-Module:
db_mod = DB_Handler()


# NL-Modules:
nl_filter = NL_Filter()
nl_sql = NL_SQL_Transformer()
sql_nl = SQL_NL_Transformer()

# UML-Modules:
sql_uml = SQL_UML_Transformer()
uml_sql = UML_SQL_Transformer()


# Orginal UML:
with open(folder +"\\UML_test_sample.txt") as file:
	original_uml = file.read()


# Original NL-Text:
with open(folder +"\\NL_test_sample.txt") as file:
	lines = file.readlines()
	original_nl = []
	for l in lines:
		l = l.replace("\n","")
		original_nl.append(l)



###############################

project_name = "small_testing"
plant_uml = original_uml


db_mod.create_new_project(project_name)
db_mod.set_curr_project(project_name)
# UML -> DB:
"""sql_statements = uml_sql.plantuml_to_sql(plant_uml)
db_mod.write_to_db(sql_statements)"""

# NL -> DB:
# Filter NL:	
filtered_nl = nl_filter.filter_nl(original_nl)
sql_queues = nl_sql.transform_nl_sql(filtered_nl)
db_mod.truncate_tables()
db_mod.write_to_db(sql_queues)


#################
df = db_mod.read_all_db()
#print(df)

# SQL -> UML:
uml_new = sql_uml.sql_to_plantuml(df)
print(uml_new)


# SQL -> NL:

nl_new = sql_nl.transform_sql_nl(df)
						
"""for line in nl_new:
	print(line)"""


############################################################################


#test_sentence = ["A week statistic can have a day statistic."]
#test_sentence = ["A day statistic is part of a week statistic."]
#test_sentence = ["A Customer can buy a vehicle"]
#test_sentence = ["A vehicle can be bought by a customer"]

"""filter_test = nl_filter.filter_nl(test_sentence)

sql_queues = nl_sql.transform_nl_sql(filter_test)"""
"""for i in sql_queues:
	print(i)"""
#db_mod.write_to_db(sql_queues)


#SQL -> NL:
"""df = db_mod.read_all_db()
nl_new = sql_nl.transform_sql_nl(df)
						
for line in nl_new:
	print(line)"""



############################################################################

db_mod.delete_db_file(project_name)
