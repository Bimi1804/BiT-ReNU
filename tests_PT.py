# Performance Tests

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)
PT_folder = main_folder + "\\Test_files\\PT"

#------------------------------ Import Modules --------------------------------#

import time
from memory_profiler import memory_usage
import csv


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

# ---- Simple Transformation functions ---- #
def nl_to_uml(input_NL):
	# NL -> SQL:
	filtered_nl = nl_filter.filter_nl(input_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	output_UML = sql_uml.sql_to_plantuml(df)
	return output_UML

def uml_to_nl(input_UML):
	# UML -> SQL:
	sql_statements = uml_sql.plantuml_to_sql(input_UML)
	db_mod.write_to_db(sql_statements)
	# SQL-> NL:
	df = db_mod.read_all_db()
	output_NL = sql_nl.transform_sql_nl(df)
	return output_NL

# ---- Memory Measure function ---- #

def measure_memory(func, *args, **kwargs):
    mem_usage, retval = memory_usage((func, args, kwargs), interval=0.1, retval=True)
    return max(mem_usage), retval

# ---- Time Measure Transformation functions ---- #

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
	return execution_time, output_NL

def nl_to_uml_timed(input_NL):
	start_time = time.time()
	# NL -> SQL:
	filtered_nl = nl_filter.filter_nl(input_NL)
	sql_queues = nl_sql.transform_nl_sql(filtered_nl)
	db_mod.write_to_db(sql_queues)
	# SQL -> UML:
	df = db_mod.read_all_db()
	output_UML = sql_uml.sql_to_plantuml(df)
	end_time = time.time()
	execution_time = end_time - start_time
	return execution_time, output_UML

# ---- Performance Test functions ---- #

def performance_test_UML_to_NL(project_name, iterations=50):
	print(f"Running Test: {project_name}, iterations = {iterations}")
	with open(f"{PT_folder}\\{project_name}\\input_UML_{project_name}.txt") as file:
		input_UML = file.read()
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	time_list = []
	memory_list = []
	for i in range(iterations):
		memory,output_NL = measure_memory(uml_to_nl,input_UML)
		memory_list.append(memory)
		db_mod.truncate_tables()
		time,output_NL = uml_to_nl_timed(input_UML)
		time_list.append(time)
		db_mod.truncate_tables()
		print(f"{i}: time = {time:.2f}s, memory = {memory:.2f} MiB")
	db_mod.delete_db_file(project_name)
	with open(f"{PT_folder}\\{project_name}\\measures_{project_name}.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		# Write the header
		writer.writerow(["time", "memory"])
		# Write the data from the lists
		for time, memory in zip(time_list, memory_list):
			writer.writerow([time, memory])
	with open(f"{PT_folder}\\{project_name}\\output_NL_{project_name}.txt", "w") as file:
		for line in output_NL:
			file.write(f"{line}\n")
	return 


def performance_test_NL_to_UML(project_name, iterations=50):
	print(f"Running Test: {project_name}, iterations = {iterations}")
	with open(f"{PT_folder}\\{project_name}\\input_NL_{project_name}.txt") as file:
		lines = file.readlines()
		input_NL = []
		for l in lines:
			l = l.replace("\n","")
			input_NL.append(l)
	db_mod.create_new_project(project_name)
	db_mod.set_curr_project(project_name)
	time_list = []
	memory_list = []
	for i in range(iterations):
		memory,output_UML = measure_memory(nl_to_uml,input_NL)
		memory_list.append(memory)
		db_mod.truncate_tables()
		time,output_UML = nl_to_uml_timed(input_NL)
		time_list.append(time)
		db_mod.truncate_tables()
		print(f"{i}: time = {time:.2f}s, memory = {memory:.2f}MiB")
	db_mod.delete_db_file(project_name)
	with open(f"{PT_folder}\\{project_name}\\measures_{project_name}.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		# Write the header
		writer.writerow(["time", "memory"])
		# Write the data from the lists
		for time, memory in zip(time_list, memory_list):
			writer.writerow([time, memory])
	with open(f"{PT_folder}\\{project_name}\\output_UML_{project_name}.txt", "w") as file:
		file.write(output_UML)
	return 


#--------------------------- Perform Tests ----------------------------#

if __name__ == '__main__':
	# ---- PT01: UML to NL, size: X ---- #
	#performance_test_UML_to_NL("PT01")

	# ---- PT02: UML to NL, size: X*2 ---- #

	# ---- PT03: UML to NL, size: X*4 ---- #

	# ---- PT04: NL to UML, size: Y ---- #
	#performance_test_NL_to_UML("PT04")

	# ---- PT05: NL to UML, size: Y*2 ---- #

	# ---- PT06: NL to UML, size: Y*4 ---- #


		




