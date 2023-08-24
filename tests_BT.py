# Tests for bidirectional transformation of BiT-ReNU:

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)
BT_folder = main_folder + "\\Test-files\\BT"


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
	# SQL->NL:
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
	return intermediary_NL, final_UML

#--------------------------- Perform Tests ------------------------------------#

# ----  BT.01 ---- #
uml_input_path = BT_folder+"\\BT_01\\input_BT01.txt"
intermediary_NL, final_UML = bt_01(uml_input_path)

