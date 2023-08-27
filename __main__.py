# BiT-ReNU

#------------------------------ Folder Paths ----------------------------------#
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)

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

#------------------------------ define basic functions ------------------------#
def uml_to_nl(uml_input, project_name="UML_project"):
    # Set up new project:
    db_mod.create_new_project(project_name)
    db_mod.set_curr_project(project_name)
    # UML -> SQL:
    sql_statements = uml_sql.plantuml_to_sql(uml_input)
    db_mod.write_to_db(sql_statements)
    # SQL-> NL:
    df = db_mod.read_all_db()
    final_NL = sql_nl.transform_sql_nl(df)
    # Delete project DB:
    db_mod.delete_db_file(project_name)
    return final_NL


def nl_to_uml(nl_input, project_name="NL_project"):
    # Set up new project:
    db_mod.create_new_project(project_name)
    db_mod.set_curr_project(project_name)
    # NL -> SQL:
    filtered_nl = nl_filter.filter_nl(nl_input)
    sql_queues = nl_sql.transform_nl_sql(filtered_nl)
    db_mod.write_to_db(sql_queues)
    # SQL -> UML:
    df = db_mod.read_all_db()
    final_UML = sql_uml.sql_to_plantuml(df)
    # Delete project DB:
    db_mod.delete_db_file(project_name)
    return final_UML

#------------------------------------------------------------------------------#

PT_folder = main_folder + "\\Test_files\\PT"

with open(f"{PT_folder}\\PT02\\input_NL_PT02.txt") as file:
    lines = file.readlines()
    nl_input = []
    for l in lines:
        l = l.replace("\n","")
        nl_input.append(l)


transformed_UML = nl_to_uml(nl_input)
print(transformed_UML)



with open(f"{PT_folder}\\PT05\\input_UML_PT05.txt") as file:
    uml_input = file.read()

transformed_NL = uml_to_nl(uml_input)
"""for i in transformed_NL:
    print(i)
"""
