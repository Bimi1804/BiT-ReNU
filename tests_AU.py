# Tests for altering in UML class model

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)
AU_folder = main_folder + "\\Test_files\\AU"


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

def check_NL_difference(original_NL,changed_NL):
	"""
	Check the difference between two sets of requirements in NL.

	Parameters
	----------
	original_NL : list[str]
	    The original list of requirements.
	changed_NL : list[str]
	    The changed list of requirements.

	Returns
	-------
	only_original : list[str]
	    A list of sentences, that appear only in the original NL.
	only_changed : list[str]
	    A list of sentences, that appear only in the changed NL.
	"""
	original_set = set(original_NL)
	changed_set = set(changed_NL)
	only_original = list(original_set - changed_set)
	only_changed = list(changed_set - original_set)
	return only_original,only_changed

def transform_UML_to_NL(original_NL_path,project_name):
	"""
	Transform a changed UML class model into NL and compare the resulting NL
	with the original NL.

	Parameters
	----------
	original_NL_path : str
	    The path to the original set of requirements.

	project_name : str
	    A name for the proejct. Used for naming the database and for finding the
	    folder of the used and created files.

	Created Files
	-------------
	final_NL_{project_name}.txt
		The final transformed NL.   

	differences_{project_name}.txt
		The differences between the original NL and the final NL.		
	"""
	# get original NL:
	with open(original_NL_path) as file:
		lines = file.readlines()
		original_NL = []
		for l in lines:
			l = l.replace("\n","")
			original_NL.append(l)
	# get changed UML:
	input_UML_path = AU_folder+f"\\{project_name}\\changed_UML_{project_name}.txt"
	with open(input_UML_path) as file:
		changed_UML = file.read()
	# Set up new project:
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(changed_UML)
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	final_NL = sql_nl.transform_sql_nl(df)
	# Compare original NL and new NL:
	only_original,only_new = check_NL_difference(original_NL,final_NL)
	# Save final_NL in .txt file:
	with open(AU_folder+f"\\{project_name}\\final_NL_{project_name}.txt", "w") as file:
		for line in final_NL:
			file.write(f"{line}\n")
	# Save differences between original and new NL in .txt file:
	with open(AU_folder+f"\\{project_name}\\differences_{project_name}.txt", "w") as file:
		file.write("Sentences only in Original NL:\n")
		for line in only_original:
			file.write(f"{line}\n")
		file.write("\n")
		file.write("Sentences only in new NL:\n")
		for line in only_new:
			file.write(f"{line}\n")
	return



#--------------------------- Perform Tests ------------------------------------#
# Define original NL file:
original_NL_path = AU_folder+"\\input_AU.txt"

# ---- AU.01: Add Class ---- #
#transform_UML_to_NL(original_NL_path,"AU01")

# ---- AU.02: Edit Class name ---- #
#transform_UML_to_NL(original_NL_path,"AU02")

# ---- AU.03: Delete Class ---- #
#transform_UML_to_NL(original_NL_path,"AU03")

# ---- AU.04: Add Attribute ---- #
#transform_UML_to_NL(original_NL_path,"AU04")

# ---- AU.05: Edit Attribute name ---- #
#transform_UML_to_NL(original_NL_path,"AU05")

# ---- AU.06: Delete Attribute ---- #
#transform_UML_to_NL(original_NL_path,"AU06")

# ---- AU.07: Add Association ---- #
#transform_UML_to_NL(original_NL_path,"AU07")

# ---- AU.08: Edit Association Name ---- #
#transform_UML_to_NL(original_NL_path,"AU08")

# ---- AU.09: Edit Association End  ---- #
#transform_UML_to_NL(original_NL_path,"AU09")

# ---- AU.10: Edit Association End Multiplicity ---- #
#transform_UML_to_NL(original_NL_path,"AU10")

# ---- AU.11: Delete Association ---- #
#transform_UML_to_NL(original_NL_path,"AU11")

# ---- AU.12: Delete Association End Multiplicity ---- #
#transform_UML_to_NL(original_NL_path,"AU12")

# ---- AU.13: Add Composition ---- #
#transform_UML_to_NL(original_NL_path,"AU13")

# ---- AU.14: Edit Composition End ---- #
#transform_UML_to_NL(original_NL_path,"AU14")

# ---- AU.15: Edit Composition End Multiplicity ---- #
#transform_UML_to_NL(original_NL_path,"AU15")

# ---- AU.16: Delete Composition ---- #
#transform_UML_to_NL(original_NL_path,"AU16")

# ---- AU.17: Delete Composition End Multiplicity ---- #
#transform_UML_to_NL(original_NL_path,"AU17")

# ---- AU.18: Add Generalization ---- #
#transform_UML_to_NL(original_NL_path,"AU18")

# ---- AU.19: Edit Generalization End ---- #
#transform_UML_to_NL(original_NL_path,"AU19")

# ---- AU.20: Delete Generalization ---- #
#transform_UML_to_NL(original_NL_path,"AU20")



