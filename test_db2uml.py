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


db_mod.set_curr_project("test_req1")


dataframes = db_mod.read_all_db()


classes = []
for index, row in dataframes[0].iterrows():
	classes.append(row[0])
attributes = []
for index,row in dataframes[1].iterrows():
	attributes.append([row[0],row[1]])
operations = []
for index,row in dataframes[2].iterrows():
	operations.append([row[0],row[1]])

generalization = []
for index, row in dataframes[3].iterrows():
	if row[1] == "generalization":
		generalization.append([row[2],row[3]])
composition = []
for index, row in dataframes[3].iterrows():
	if row[1] == "composition":
		composition.append([row[2], row[3]])
associations = []
for index, row in dataframes[3].iterrows():
	if row[1] == "association":
		associations.append([row[0],row[2],row[3],row[4],row[5],row[6],row[7]])



plant_class = ""
for i in classes:
	plant_class = plant_class + f"class {i}" + " {\n"
	for attr in attributes:
		if attr[1] == i:
			plant_class = plant_class +f"+ {attr[0]}\n"
	for opr in operations:
		if opr[1] == i:
			plant_class = plant_class + f"+ {opr[0]}\n"
	plant_class = plant_class + "}\n\n"


plant_asc = ""
for i in generalization:
	plant_asc = plant_asc + f"{i[1]} <|-- {i[0]}\n"

for i in composition:
	plant_asc = plant_asc + f"{i[1]} *-- {i[0]}\n"

for i in associations:
	plant_asc = plant_asc + f"{i[1]} \"{i[3]}..{i[4]}\" -- \"{i[5]}..{i[6]}\" {i[2]}: {i[0]}\n"

project_title = "TEST"
plantuml = f"@startuml\n\ntitle {project_title}\n\n{plant_class}{plant_asc}\n@enduml"

print(plantuml)

