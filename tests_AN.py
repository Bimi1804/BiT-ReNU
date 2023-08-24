# Tests for altering requirements in NL:

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)
AN_folder = main_folder + "\\Test_files\\AN"


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

# ---- General functions to add/delete whole sentences ----#
def add_sentence(transformed_NL,sentence):
	changed_NL = transformed_NL
	changed_NL.append(sentence)
	return changed_NL

def delete_sentence(transformed_NL,sentence):
	changed_NL = transformed_NL
	changed_NL.remove(sentence)
	return changed_NL

def change_sentence(uml_input_path,change_type,sentence,project_name):
	# get input UML:
	with open(uml_input_path) as file:
		uml_input = file.read()
	# Set up new project:
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(uml_input)
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	transformed_NL = sql_nl.transform_sql_nl(df)
	# Add sentence:
	if change_type == "add":
		changed_NL = add_sentence(transformed_NL,sentence)
	# Delete sentence:
	if change_type == "delete":
		changed_NL = delete_sentence(transformed_NL,sentence)
	# changed_NL -> SQL:
	filtered_nl = nl_filter.filter_nl(changed_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.truncate_tables()
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	final_UML = sql_uml.sql_to_plantuml(df)
	db_mod.delete_db_file(project_name)
	# Save intermediary NL and final UML class model in .txt files:
	with open(AN_folder+ f"\\{project_name}\\transformed_NL.txt", "w") as file:
		for line in transformed_NL:
			file.write(f"{line}\n")
	with open(AN_folder+ f"\\{project_name}\\changed_NL.txt", "w") as file:
		for line in changed_NL:
			file.write(f"{line}\n")
	with open(AN_folder+ f"\\{project_name}\\final_UML.txt", "w") as file:
		file.write(final_UML)
	return

# ---- Specific Test functions ---- #
def an_01(uml_input_path,sentence):
	change_sentence(uml_input_path,"add",sentence,"AN01")
	return

def an_02(uml_input_path,sentence):
	change_sentence(uml_input_path,"delete",sentence,"AN02")
	return

def an_03(uml_input_path,sentence):
	change_sentence(uml_input_path,"add",sentence,"AN03")
	return

def an_04(uml_input_path,sentence):
	change_sentence(uml_input_path,"delete",sentence,"AN04")
	return



#--------------------------- Perform Tests ------------------------------------#

# Define input file for all tests:
input_UML_path = AN_folder+"\\input_AN.txt"

# ---- AN.01: Add Active Association ---- #
an_01(input_UML_path,"A customer must drive a vehicle.")

# ---- AN.02: Delete Active Association ---- #
an_02(input_UML_path,"A vehicle purchase must sell a vehicle.")

# ---- AN.03: Add Passive Association ---- #
an_03(input_UML_path,"A vehicle can be driven by a customer.")

# ---- AN.04: Delete Passive Association ---- #
an_04(input_UML_path,"A vehicle purchase must be made by a customer.")

# ---- AN.05: Add Attribute ---- #

# ---- AN.06: Delete Attribute ---- #

# ---- AN.07: Add Generalization ---- #

# ---- AN.08: Delete Generalization ---- #

# ---- AN.09: Add Composition – Part of Whole ---- #

# ---- AN.10: Delete Composition – Part of Whole ---- #

# ---- AN.11: Add Composition – Whole has Part ---- #

# ---- AN.12: Delete Composition – Whole has Part ---- #
