# Tests for bidirectional transformation of BiT-ReNU:

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)
BT_folder = main_folder + "\\Test_files\\BT"


#------------------------------ Import Modules --------------------------------#
from python_scripts.DB_module import *
from python_scripts.NL_module import *
from python_scripts.UML_module import *

#------------------------------ Initiate Modules ------------------------------#
# DB-Module:
db_mod = DB_Handler()
# NL-Module:
nl_filter = NL_Filter()
nl_sql = NL_SQL_Transformer()
sql_nl = SQL_NL_Transformer()
# UML-Module:
sql_uml = SQL_UML_Transformer()
uml_sql = UML_SQL_Transformer()

#--------------------------- Define Test-Functions ----------------------------#

def bt_01(uml_input_path):
	# get input UML:
	with open(uml_input_path) as file:
		uml_input = file.read()
	# Set up new project:
	project_name = "bt_01"
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(uml_input)
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	intermediary_NL = sql_nl.transform_sql_nl(df)
	# NL -> SQL:
	filtered_nl = nl_filter.filter_nl(intermediary_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.truncate_tables()
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	final_UML = sql_uml.sql_to_plantuml(df)
	db_mod.delete_db_file(project_name)
	# Save intermediary NL and final UML class model in .txt files:
	with open(BT_folder+"\\BT_01\\intermediary_NL.txt", "w") as file:
		for line in intermediary_NL:
			file.write(f"{line}\n")
	with open(BT_folder+"\\BT_01\\final_UML.txt", "w") as file:
		file.write(final_UML)
	return 


def bt_02(nl_input_path):
	# get input NL:
	with open(nl_input_path) as file:
		lines = file.readlines()
		nl_input = []
		for l in lines:
			l = l.replace("\n","")
			nl_input.append(l)
	# Set up new project:
	project_name = "bt_02"
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	# NL -> SQL:
	filtered_nl = nl_filter.filter_nl(nl_input)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	intermediary_UML = sql_uml.sql_to_plantuml(df)
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(intermediary_UML)
	db_mod.truncate_tables()
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	final_NL = sql_nl.transform_sql_nl(df)
	db_mod.delete_db_file(project_name)
	# Save intermediary UML and final NL in .txt files:
	with open(BT_folder+"\\BT_02\\intermediary_UML.txt", "w") as file:
		file.write(intermediary_UML)
	with open(BT_folder+"\\BT_02\\final_NL.txt", "w") as file:
		for line in final_NL:
			file.write(f"{line}\n")
	return 

#--------------------------- Perform Tests ------------------------------------#

# ----  BT.01 ---- #
bt_01(BT_folder+"\\BT_01\\input_BT01.txt")

# ----  BT.02 ---- #
bt_02(BT_folder+"\\BT_02\\input_BT02.txt")




