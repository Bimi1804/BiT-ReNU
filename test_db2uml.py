# TEST DB2UML

import pandas as pd 
import os

from python_scripts.DB_module import *
from python_scripts.NL_module import *
from python_scripts.UML_module import *


db_mod = DB_Handler()
NL_filter = NL_Filter()
NL_SQL_transformer = NL_SQL_Transformer()
SQL_NL_morph = SQL_NL_Transformer()
SQL_UML_transformer = SQL_UML_Transformer()
UML_SQL_transformer = UML_SQL_Transformer()

db_mod.delete_db_file("test_req1")

db_mod.create_new_project("test_req1")
db_mod.set_curr_project("test_req1")


with open(os.getcwd()+"\\test_cases\\plant_test_requirements.txt") as file:
	plant_text = file.read()

sql_statemens = UML_SQL_transformer.plantuml_to_sql(plant_text)

db_mod.write_to_db(sql_statemens)

dataframes = db_mod.read_all_db()
plant_dia = SQL_UML_transformer.sql_to_plantuml(dataframes)
print(plant_dia)



counter = 1
for i in SQL_NL_morph.attr_to_nl(dataframes[1]):
	print(f"{counter}: {i}")
	counter = counter +1

gen_sent, comp_sent, asc_sent = SQL_NL_morph.asc_to_nl(dataframes[3])
for i in gen_sent:
	print(f"{counter}: {i}")
	counter = counter +1
for i in comp_sent:
	print(f"{counter}: {i}")
	counter = counter +1
for i in asc_sent:
	print(f"{counter}: {i[0]}")
	counter = counter +1
	print(f"{counter}: {i[1]}")
	counter = counter +1

