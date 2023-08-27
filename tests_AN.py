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
def change_sentence(uml_input_path,change_type,sentence,project_name,edited_sentence=""):
	"""
	1. Transform a UML into NL.
	2. Change a sentence in the transformed NL. Change can be:
		- Add a sentence
		- Delete a sentence
		- Edit a sentence
	3. Transformed the change NL back into UML.
	4. Save files to the test-folder with the project_name:
		- transformed_NL.txt : The transformed NL without changes.
		- changed_NL.txt : The transformed NL with changes.
		- final_UML.txt : The UML, transformed from the changed NL.

	Parameters
	----------
	uml_input_path : str
		The path to the UML input file.

	change_type : str
		The type of change that should be done. Can have one of three values:
			- "add" : To add a sentence
			- "delete" : To delete a sentence
			- "edit" : To edit a sentence (requires edited_sentence)

	sentence : str
		The sentence that should be changed.

	project_name : str
		The name of the test. Used to find the right folder and to create the 
		database.

	edited_sentence : str
		If a sentence should be edited. This is the new version of the sentence.

	Created Files
	-------------
	transformed_NL.txt
		The transformed NL without changes.
	changed_NL.txt
		The transformed NL with changes.
	final_UML.txt
		The UML, transformed from the changed NL.
	"""

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
		changed_NL.append(sentence)
	# Delete sentence:
	if change_type == "delete":
		changed_NL.remove(sentence)
	# Edit sentence:
	if change_type == "edit":
		index = changed_NL.index(sentence)
		changed_NL[index] = edited_sentence
	# changed_NL -> SQL:
	filtered_nl = nl_filter.filter_nl(changed_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.truncate_tables()
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	final_UML = sql_uml.sql_to_plantuml(df)
	db_mod.delete_db_file(project_name)
	# Save files to right Test-folder:
	with open(AN_folder+ f"\\{project_name}\\transformed_NL.txt", "w") as file:
		for line in transformed_NL:
			file.write(f"{line}\n")
	with open(AN_folder+ f"\\{project_name}\\changed_NL.txt", "w") as file:
		for line in changed_NL:
			file.write(f"{line}\n")
	with open(AN_folder+ f"\\{project_name}\\final_UML.txt", "w") as file:
		file.write(final_UML)
	return

# ---- Specific Test functions: Add/Delete whole sentences ---- #
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

def an_05(uml_input_path,sentence):
	change_sentence(uml_input_path,"add",sentence,"AN05")
	return

def an_06(uml_input_path,sentence):
	change_sentence(uml_input_path,"delete",sentence,"AN06")
	return

def an_07(uml_input_path,sentence):
	change_sentence(uml_input_path,"add",sentence,"AN07")
	return

def an_08(uml_input_path,sentence):
	change_sentence(uml_input_path,"delete",sentence,"AN08")
	return

def an_09(uml_input_path,sentence):
	change_sentence(uml_input_path,"add",sentence,"AN09")
	return

def an_10(uml_input_path,sentence):
	change_sentence(uml_input_path,"delete",sentence,"AN10")
	return

def an_11(uml_input_path,sentence):
	change_sentence(uml_input_path,"add",sentence,"AN11")
	return

def an_12(uml_input_path,sentence):
	change_sentence(uml_input_path,"delete",sentence,"AN12")
	return

# ---- Specific Test functions: Edit Sentence Elements ---- #
def an_13(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN13", edited_sentence)
	return

def an_14(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN14", edited_sentence)
	return
	
def an_15(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN15", edited_sentence)
	return
	
def an_16(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN16", edited_sentence)
	return
	
def an_17(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN17", edited_sentence)
	return
	
def an_18(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN18", edited_sentence)
	return
	
def an_19(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN19", edited_sentence)
	return
	
def an_20(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN20", edited_sentence)
	return
	
def an_21(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN21", edited_sentence)
	return
	
def an_22(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN22", edited_sentence)
	return
	
def an_23(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN23", edited_sentence)
	return
	
def an_24(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN24", edited_sentence)
	return
	
def an_25(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN25", edited_sentence)
	return
	
def an_26(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN26", edited_sentence)
	return
	
def an_27(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN27", edited_sentence)
	return
	
def an_28(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN28", edited_sentence)
	return
	
def an_29(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN29", edited_sentence)
	return
	
def an_30(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN30", edited_sentence)
	return
	
def an_31(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN31", edited_sentence)
	return
	
def an_32(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN32", edited_sentence)
	return
	
def an_33(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN33", edited_sentence)
	return
	
def an_34(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN34", edited_sentence)
	return
	
def an_35(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN35", edited_sentence)
	return
	
def an_36(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN36", edited_sentence)
	return
	
def an_37(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN37", edited_sentence)
	return
	
def an_38(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN38", edited_sentence)
	return
	
def an_39(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN39", edited_sentence)
	return
	
def an_40(uml_input_path,sentence,edited_sentence):
	change_sentence(uml_input_path, "edit", sentence, "AN40", edited_sentence)
	return


#--------------------------- Perform Tests ------------------------------------#

# Define input file for all tests:
input_UML_path = AN_folder+"\\input_AN.txt"

#--------------------------- Add/Delete Sentences -----------------------------#
# ---- AN.01: Add Active Association ---- #
#an_01(input_UML_path,"A customer must drive a vehicle.")

# ---- AN.02: Delete Active Association ---- #
#an_02(input_UML_path,"A vehicle purchase must sell a vehicle.")

# ---- AN.03: Add Passive Association ---- #
#an_03(input_UML_path,"A vehicle can be driven by a customer.")

# ---- AN.04: Delete Passive Association ---- #
#an_04(input_UML_path,"A vehicle purchase must be made by a customer.")

# ---- AN.05: Add Attribute ---- #
#an_05(input_UML_path,"An Employee has a name.")

# ---- AN.06: Delete Attribute ---- #
#an_06(input_UML_path,"A customer has a name.")

# ---- AN.07: Add Generalization ---- #
#an_07(input_UML_path,"An Employee is a Customer.")

# ---- AN.08: Delete Generalization ---- #
#an_08(input_UML_path,"A day statistic is a sale statistic.")

# ---- AN.09: Add Composition – Part of Whole ---- #
#an_09(input_UML_path,"A vehicle is part of a vehicle purchase.")

# ---- AN.10: Delete Composition – Part of Whole ---- #
#an_10(input_UML_path,"A day statistic is part of a week statistic.")

# ---- AN.11: Add Composition – Whole has Part ---- #
#an_11(input_UML_path,"A vehicle purchase must have a vehicle.")

# ---- AN.12: Delete Composition – Whole has Part ---- #
#an_12(input_UML_path,"A week statistic must have a day statistic.")




#--------------------------- Edit Sentence Elements ---------------------------#


# ---- AN.13: Active Association: Edit Subject – new subject exists ---- #
#an_13(input_UML_path,
#	"An employee can advise a vehicle purchase.",
#	"A customer can advise a vehicle purchase.")

# ---- AN.14: Active Association: Edit Subject – new subject does not exist ---- #
#an_14(input_UML_path,
#	"An employee can advise a vehicle purchase.",
#	"A boss can advise a vehicle purchase.")

# ---- AN.15: Active Association: Switch modal verb ---- #
#an_15(input_UML_path,
#	"An employee can advise a vehicle purchase.",
#	"An employee must advise a vehicle purchase.")

# ---- AN.16: Active Association: Edit Action ---- #
#an_16(input_UML_path,
#	"An employee can advise a vehicle purchase.",
#	"An employee can support a vehicle purchase.")

# ---- AN.17: Active Association: Edit Object – new object exists ---- #
#an_17(input_UML_path,
#	"An employee can advise a vehicle purchase.",
#	"An employee can advise a vehicle.")

# ---- AN.18: Active Association: Edit Object– new object does not exist ---- #
#an_18(input_UML_path,
#	"An employee can advise a vehicle purchase.",
#	"An employee can advise a competitor.")

# ---- AN.19: Passive Association: Edit Subject – new subject exists ---- #
#an_19(input_UML_path,
#	"A vehicle purchase must be advised by an employee.",
#	"A vehicle must be advised by an employee.")

# ---- AN.20: Passive Association: Edit Subject– new subject does not exist ---- #
#an_20(input_UML_path,
#	"A vehicle purchase must be advised by an employee.",
#	"A competitor must be advised by an employee.")

# ---- AN.21: Passive Association: Switch modal verb ---- #
#an_21(input_UML_path,
#	"A vehicle purchase must be advised by an employee.",
#	"A vehicle purchase can be advised by an employee.")

# ---- AN.22: Passive Association: Edit Action ---- #
#an_22(input_UML_path,
#	"A vehicle purchase must be advised by an employee.",
#	"A vehicle purchase must be supported by an employee.")

# ---- AN.23: Passive Association: Edit Object – new object exists ---- #
#an_23(input_UML_path,
#	"A vehicle purchase must be advised by an employee.",
#	"A vehicle purchase must be advised by a customer.")

# ---- AN.24: Passive Association: Edit Object – new object does not exist ---- #
#an_24(input_UML_path,
#	"A vehicle purchase must be advised by an employee.",
#	"A vehicle purchase must be advised by a boss.")

# ---- AN.25: Attribute: Edit Subject – new subject exists ---- #
#an_25(input_UML_path,
#	"A sale statistic has a sale.",
#	"A day statistic has a sale.")

# ---- AN.26: Attribute: Edit Subject – new subject does not exist ---- #
#an_26(input_UML_path,
#	"A sale statistic has a sale.",
#	"A sale record has a sale.")

# ---- AN.27: Attribute: Edit Object ---- #
#an_27(input_UML_path,
#	"A sale statistic has a sale.",
#	"A sale statistic has a date.")

# ---- AN.28: Generalization: Edit Subject – new subject exists ---- #
#an_28(input_UML_path,
#	"A motorcycle is a vehicle.",
#	"An Employee is a vehicle.")

# ---- AN.29: Generalization: Edit Subject – new subject does not exist ---- #
#an_29(input_UML_path,
#	"A motorcycle is a vehicle.",
#	"A bike is a vehicle.")

# ---- AN.30: Generalization: Edit Object – new object exists ---- #
#an_30(input_UML_path,
#	"A motorcycle is a vehicle.",
#	"A motorcycle is a passenger vehicle.")

# ---- AN.31: Generalization: Edit Object – new object does not exist ---- #
#an_31(input_UML_path,
#	"A motorcycle is a vehicle.",
#	"A motorcycle is a bike.")

# ---- AN.32: Composition T.5: Edit Subject – new subject exists ---- #
#an_32(input_UML_path,
#	"A day statistic is part of a week statistic.",
#	"A vehicle purchase is part of a week statistic.")

# ---- AN.33: Composition T.5: Edit Subject – new subject does not exist ---- #
#an_33(input_UML_path,
#	"A day statistic is part of a week statistic.",
#	"A week record is part of a week statistic.")

# ---- AN.34: Composition T.5: Edit Object– new object exists ---- #
#an_34(input_UML_path,
#	"A day statistic is part of a week statistic.",
#	"A day statistic is part of a vehicle purchase.")

# ---- AN.35: Composition T.5: Edit Object – new object does not exist ---- #
#an_35(input_UML_path,
#	"A day statistic is part of a week statistic.",
#	"A day statistic is part of a week record.")

# ---- AN.36: Composition T.6: Edit Subject – new subject exists ---- #
#an_36(input_UML_path,
#	"A week statistic must have a day statistic.",
#	"A vehicle purchase must have a day statistic.")

# ---- AN.37: Composition T.6: Edit Subject – new subject does not exist ---- #
#an_37(input_UML_path,
#	"A week statistic must have a day statistic.",
#	"A week record must have a day statistic.")

# ---- AN.38: Composition T.6: Edit Object– new object exists ---- #
#an_38(input_UML_path,
#	"A week statistic must have a day statistic.",
#	"A week statistic must have a vehicle purchase.")

# ---- AN.39: Composition T.6: Edit Object – new object does not exist ---- #
#an_39(input_UML_path,
#	"A week statistic must have a day statistic.",
#	"A week statistic must have a week record.")

# ---- AN.40: Composition T.6: Switch modal verb ---- #
#an_40(input_UML_path,
#	"A week statistic must have a day statistic.",
#	"A week statistic can have a day statistic.")







