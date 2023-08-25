# Performance Tests

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)
PT_folder = main_folder + "\\Test_files\\PT"

#------------------------------ Import testing tools --------------------------#

import time
from memory_profiler import memory_usage


#------------------------------ Import BiT-ReNU -------------------------------#
from python_scripts.DB_module import *
from python_scripts.NL_module import *
from python_scripts.UML_module import *



#------------------------------ Initiate BiT-ReNU -----------------------------#
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


def nl_to_uml(input_NL):
	# NL -> SQL:
	filtered_nl = nl_filter.filter_nl(input_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	final_UML = sql_uml.sql_to_plantuml(df)
	return output_UML

def uml_to_nl(input_UML):
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(input_UML)
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	output_NL = sql_nl.transform_sql_nl(df)
	return output_NL

def measure_memory(func, *args, **kwargs):
    mem_usage, retval = memory_usage((func, args, kwargs), interval=0.1, retval=True)
    return mem_usage, retval

def uml_to_nl_timed(input_UML):
	start_time = time.time()
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(input_UML)
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	output_NL = sql_nl.transform_sql_nl(df)
	end_time = time.time()
	execution_time = end_time - start_time
	return output_NL,execution_time

def nl_to_uml_timed(input_NL):
	start_time = time.time()
	# NL -> SQL:
	filtered_nl = nl_filter.filter_nl(input_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	final_UML = sql_uml.sql_to_plantuml(df)
	end_time = time.time()
	execution_time = end_time - start_time
	return output_UML,execution_time



if __name__ == '__main__':
	uml_input_path = PT_folder + "\\input_UML.txt"

	# get input UML:
	with open(uml_input_path) as file:
		input_UML = file.read()
		
	# Set up new project:
	project_name = "PT01"
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	memory, duration, retval = measure_function(uml_to_nl,input_UML)
	print(f"Memory used: {memory:.2f} MiB")
	print(f"Execution time: {duration} seconds")
	print(f"Execution time: {retval} seconds")


