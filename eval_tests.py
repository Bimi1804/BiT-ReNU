# Evaluation Tests:
import os

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

# Original NL-Text:
with open(os.getcwd()+"\\test_cases\\test_requirements_NL.txt") as file:
	lines = file.readlines()
	original_nl = []
	for l in lines:
		l = l.replace("\n","")
		original_nl.append(l)



# NL -> UML 
def test_nl_uml(original_nl):
	# create new project and connect:
	db_mod.create_new_project("test_01")
	db_mod.set_curr_project("test_01")
	# Filter NL:	
	filtered_nl = nl_filter.filter_nl(original_nl)
	# NL -> DB:
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# DB -> UML:
	dataframes = db_mod.read_all_db()
	plant_og = sql_uml.sql_to_plantuml(dataframes)
	# Clean-Up:
	db_mod.delete_db_file("test_01")
	return plant_og

# NL -> UML (change element) -> NL
def test_uml_nl(original_nl,plant_changed,project_name):
	# create new project and connect:
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	# Filter NL:	
	filtered_nl = nl_filter.filter_nl(original_nl)
	# NL -> DB:
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(plant_changed)
	db_mod.truncate_tables()
	db_mod.write_to_db(sql_statements)
	# SQL -> NL:
	df = db_mod.read_all_db()
	nl_new = sql_nl.transform_sql_nl(df)
	# Clean-Up:
	db_mod.delete_db_file(project_name)
	return nl_new

#---------------------------------------------

# Test_01:
plant_01 = test_nl_uml(original_nl)
with open(os.getcwd()+"\\evaluation\\plant_01.txt","w") as file:
	file.write(plant_01)


# Test_011:
with open(os.getcwd()+ "\\evaluation\\plant_011.txt") as file:
	plant_011 = file.read()
nl_011 = test_uml_nl(original_nl,plant_011,"test_011")
#for line in nl_011: print(line)


# Test_012:
with open(os.getcwd()+ "\\evaluation\\plant_012.txt") as file:
	plant_012 = file.read()
nl_012 = test_uml_nl(original_nl,plant_012,"test_012")
#for line in nl_012: print(line)

# Test_013:
with open(os.getcwd()+ "\\evaluation\\plant_013.txt") as file:
	plant_013 = file.read()
nl_013 = test_uml_nl(original_nl,plant_013,"test_013")
#for line in nl_013: print(line)

