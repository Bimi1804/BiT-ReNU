# Evaluation Tests:
import os
script_path = os.path.abspath(__file__)
folder = os.path.dirname(script_path)



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
with open(folder +"\\Manually_transformed_Tests\\test_requirements_NL.txt") as file:
	lines = file.readlines()
	original_nl = []
	for l in lines:
		l = l.replace("\n","")
		original_nl.append(l)

# Orginal UML:
with open(folder +"\\Manually_transformed_Tests\\plant_test_requirements.txt") as file:
	original_uml = file.read()



# NL -> UML 
def test_nl_uml(nl_text,project_name,plant_uml=None):
	# create new project and connect:
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	if plant_uml != None:
		sql_statements = uml_sql.plantuml_to_sql(plant_uml)
		db_mod.write_to_db(sql_statements)
	# Filter NL:	
	filtered_nl = nl_filter.filter_nl(nl_text)
	# NL -> DB:
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.truncate_tables()
	db_mod.write_to_db(sql_queues)
	# DB -> UML:
	dataframes = db_mod.read_all_db()
	uml_new = sql_uml.sql_to_plantuml(dataframes)
	# Clean-Up:
	db_mod.delete_db_file(project_name)
	return uml_new

# NL -> UML -> NL
def test_uml_nl(plant_uml,project_name,nl_text=None):
	# create new project and connect:
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	if nl_text != None:
		# Filter NL:	
		filtered_nl = nl_filter.filter_nl(nl_text)
		# NL -> DB:
		sql_queues = nl_sql.transform_nl_sql(filtered_nl)
		db_mod.write_to_db(sql_queues)
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(plant_uml)
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
plant_01 = test_nl_uml(original_nl,"test_01")
with open(folder +"\\Validation_Tests\\plant_01.txt","w") as file:
	file.write(plant_01)

# Test_011 (Change element)
with open(folder + "\\Validation_Tests\\plant_011.txt") as file:
	plant_011 = file.read()
nl_011 = test_uml_nl(plant_011,"test_011",original_nl)
#for line in nl_011: print(line)

# Test_012 (Add element)
with open(folder + "\\Validation_Tests\\plant_012.txt") as file:
	plant_012 = file.read()
nl_012 = test_uml_nl(plant_012,"test_012",original_nl)
#for line in nl_012: print(line)

# Test_013 (Delete element)
with open(folder + "\\Validation_Tests\\plant_013.txt") as file:
	plant_013 = file.read()
nl_013 = test_uml_nl(plant_013,"test_013",original_nl)
#for line in nl_013: print(line)

#------------------------------------------------------------------

# Test_02:
nl_02 = test_uml_nl(original_uml,"test_02")
with open(folder +"\\Validation_Tests\\text_020.txt","w") as file:
	for line in nl_02:
		file.write(f"{line}\n")

# Test_021 (Change requirement):
with open(folder +"\\Validation_Tests\\text_021.txt") as file:
	lines = file.readlines()
	nl_021 = []
	for l in lines:
		l = l.replace("\n","")
		nl_021.append(l)
uml_021 = test_nl_uml(nl_021,"test_021",original_uml)
#print(uml_021)

# Test_022 (Add requirement):
with open(folder +"\\Validation_Tests\\text_022.txt") as file:
	lines = file.readlines()
	nl_022 = []
	for l in lines:
		l = l.replace("\n","")
		nl_022.append(l)
uml_022 = test_nl_uml(nl_022,"test_022",original_uml)
#print(uml_022)


# Test_023 (Delete requirement):
with open(folder +"\\Validation_Tests\\text_023.txt") as file:
	lines = file.readlines()
	nl_023 = []
	for l in lines:
		l = l.replace("\n","")
		nl_023.append(l)
uml_023 = test_nl_uml(nl_023,"test_023",original_uml)
print(uml_023)