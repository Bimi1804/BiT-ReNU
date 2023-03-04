# UML Module
import pandas as pd
import os


# UML -> DB
class SQL_UML_Transformer():
	"""docstring for DB_to_UML"""
	def __init__(self):
		pass 

	def sql_to_plantuml(self,dataframes):
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

		plantuml = f"@startuml\n\n{plant_class}{plant_asc}\n@enduml"
		return plantuml


# DB -> UML