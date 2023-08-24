# UML Module

################################## Import #################################

import pandas as pd
import os

################################## Classes #################################

class SQL_UML_Transformer():

	"""
	Transform SQL into UML.

	Methods
	-------
	sql_to_plantuml(list(pandas.Dataframe)) : str
		Transform dataframes into a string for plantuml. 
	"""


	def __init__(self):
		pass 

	def sql_to_plantuml(self,dataframes):
		"""
		Transform dataframes into a string for plantuml.

		Parameters
		----------
		dataframes : list(pandas.Dataframe)
			Tables as dataframes. List elements in the following order:
				0 = classes table
				1 = attributes table
				2 = generalization table
				3 = associations table
		
		Returns
		-------
		plantuml : str
			UML class model in plantUML notation.
		"""
		classes = []
		for index, row in dataframes[0].iterrows():
			classes.append(row[0])

		attributes = []
		for index,row in dataframes[1].iterrows():
			attributes.append([row[0],row[1]])

		generalization = []
		for index, row in dataframes[2].iterrows():
				generalization.append([row[0],row[1]])

		composition = []
		for index, row in dataframes[3].iterrows():
			if row[1] == "composite":
				composition.append([row[0],row[2],row[3],row[4],row[5],row[6],row[7]])

		associations = []
		for index, row in dataframes[3].iterrows():
			if row[1] == "none":
				associations.append([row[0],row[2],row[3],row[4],row[5],row[6],row[7]])

		plant_class = ""
		for i in classes:
			plant_class = plant_class + f"class {i}" + " {\n"
			for attr in attributes:
				if attr[1] == i:
					plant_class = plant_class +f"+ {attr[0]}\n"
			plant_class = plant_class + "}\n\n"

		plant_asc = ""
		for i in generalization:
			plant_asc = plant_asc + f"{i[0]} <|-- {i[1]}\n"


		for i in composition:
			if str(i[3]) == "None" and str(i[4]) == "None" and str(i[5]) == "None" and str(i[6]) == "None":
				plant_asc = plant_asc + f"{i[1]} *-- {i[2]}\n"
			elif str(i[3]) == "None" and str(i[4]) == "None":
				plant_asc = plant_asc + f"{i[1]} *-- \"{i[5]}..{i[6]}\" {i[2]}\n"
			elif str(i[5]) == "None" and str(i[6]) == "None":
				plant_asc = plant_asc + f"{i[1]} \"{i[3]}..{i[4]}\" *-- {i[2]}\n"
			else:
				plant_asc = plant_asc + f"{i[1]} \"{i[3]}..{i[4]}\" *-- \"{i[5]}..{i[6]}\" {i[2]}\n"

		for i in associations:
			if str(i[3]) == "None" and str(i[4]) == "None" and str(i[5]) == "None" and str(i[6]) == "None":
				plant_asc = plant_asc + f"{i[1]} -- {i[2]}\n"

			if str(i[3]) == "None" and str(i[4]) == "None":
				plant_asc = plant_asc + f"{i[1]} -- \"{i[5]}..{i[6]}\" {i[2]}: {i[0]}\n"
			elif str(i[5]) == "None" and str(i[6]) == "None":
				plant_asc = plant_asc + f"{i[1]} \"{i[3]}..{i[4]}\" -- {i[2]}: {i[0]}\n"
			else:
				plant_asc = plant_asc + f"{i[1]} \"{i[3]}..{i[4]}\" -- \"{i[5]}..{i[6]}\" {i[2]}: {i[0]}\n"

		plantuml = f"@startuml\n\n{plant_class}{plant_asc}\n@enduml"
		return plantuml

class UML_SQL_Transformer():
	"""
	Transform UML to SQL.

	Methods
	--------
	plantuml_to_sql (str) : list(str)
		Transform UML class model in plantUML into SQL statements.
	"""
	def __init__(self):
		pass 

	def plantuml_to_sql(self,plant_txt):
		"""
		Transform UML class model in plantUML into SQL statements.

		Parameters
		----------
		plant_txt : str
			UML class model in plantUML notation.

		Returns
		-------
		sql_statements : list(str)
			List of SQL-statements.
		"""

		plant_txt = plant_txt.replace(" ","")
		#-------------------------
		sql_statements = []
		while "class" in plant_txt:
			class_start = plant_txt.find("class")
			class_content_start = plant_txt.find("{")
			class_content_end = plant_txt.find("}")
			class_name = plant_txt[class_start+5:class_content_start]
			class_content = plant_txt[class_content_start+1:class_content_end].replace("\n","")
			plant_txt = plant_txt[class_content_end+1:]
			class_attr = []
			while "+" in class_content:
				plus_index = []
				for i in range(len(class_content)):
					if class_content[i] == "+":
						plus_index.append(i)
				if len(plus_index) > 1:
					start = plus_index[0]
					end = plus_index[1]
					item = class_content[start+1:end]
					class_content = class_content[plus_index[1]:]
				elif len(plus_index) == 1:
					item = class_content[plus_index[0]+1:]
					class_content = ""
				if "()" not in item:
					class_attr.append(item)
			sql_statements.append(f"""INSERT OR IGNORE INTO classes(class_name) VALUES ('{class_name.replace(" ","")}')""")
			for attr in class_attr:
				if attr != "":
					sql_statements.append(f"""INSERT OR IGNORE INTO attributes(attr_name,class_name) VALUES ('{attr.replace(" ","")}','{class_name.replace(" ","")}')""")


		#-----------------------------------------------------
		generalization = []
		composition = []
		plant_asc_lines = plant_txt.splitlines()
		for line in plant_asc_lines:
			if "<|--" in line:
				generalization.append(line)
				plant_txt = plant_txt.replace(line,"")
			if "*--" in line:
				composition.append(line)
				plant_txt = plant_txt.replace(line,"")

		for gen in generalization:
			arrow = gen.find("<|--")
			sql_statements.append(f"""INSERT OR IGNORE INTO generalizations(super_class,sub_class) 
													VALUES ('{gen[:arrow]}','{gen[arrow+4:]}')""")
		for line in composition:
			mid_point = line.find("*--")
			# first part (before *--)
			first_half = line[:mid_point]
			if first_half.find('"') >= 0:
				pointer = first_half.find('"')
				class_a = first_half[:pointer]
				low_a = "1"
				up_a = "*"
			first_half = line[:mid_point]
			if first_half.find('"') < 0:
				class_a = first_half
				low_a = "1"
				up_a = "*"
			# second part (after *--)
			second_half = line[mid_point+3:]
			if second_half.find('"') >= 0:
				pointer = second_half.find('"')
				second_half = second_half[pointer:]
				pointer = second_half.find("..")
				low_b = second_half[:pointer].replace('"',"")
				second_half = second_half[pointer+2:]
				pointer = second_half.find('"')
				up_b = second_half[:pointer].replace('"',"")
				second_half = second_half[pointer+1:]
				class_b = second_half
			second_half = line[mid_point+3:]
			if second_half.find('"') < 0:
				class_b = second_half
				low_b = None
				up_b = None 
			sql_statements.append(f"""INSERT OR IGNORE INTO associations(asc_name,agg_kind,
									class_name_a,class_name_b,lower_a,upper_a,lower_b,upper_b) 
									VALUES ('is part of','composite','{class_a}','{class_b}','{low_a}','{up_a}','{low_b}','{up_b}')""")
		plant_asc_lines = plant_txt.splitlines()
		associations = []
		for line in plant_asc_lines:
			if line != "" and line != "@enduml":
				associations.append(line)
		for line in associations:
			mid_point = line.find("--")
			# first part (before --)
			first_half = line[:mid_point]
			if first_half.find('"') >= 0:
				pointer = first_half.find('"')
				class_a = first_half[:pointer]
				first_half = first_half[pointer:]
				pointer = first_half.find("..")
				low_a = first_half[:pointer].replace('"',"")
				first_half = first_half[pointer+2:]
				pointer = first_half.find('"')
				up_a = first_half[:pointer].replace('"',"")
			first_half = line[:mid_point]
			if first_half.find('"') < 0:
				class_a = first_half
				low_a = None
				up_a = None
			# second part (after --)
			second_half = line[mid_point+2:]
			if second_half.find('"') >= 0:
				pointer = second_half.find('"')
				second_half = second_half[pointer:]
				pointer = second_half.find("..")
				low_b = second_half[:pointer].replace('"',"")
				second_half = second_half[pointer+2:]
				pointer = second_half.find('"')
				up_b = second_half[:pointer].replace('"',"")
				second_half = second_half[pointer+1:]
				pointer = second_half.find(":")
				class_b = second_half[:pointer]
				asc_name = second_half[pointer+1:]
			second_half = line[mid_point+2:]
			if second_half.find('"') < 0:
				pointer = second_half.find(":")
				class_b = second_half[:pointer]
				asc_name = second_half[pointer+1:]
				low_b = None
				up_b = None 			
			sql_statements.append(f"""INSERT OR IGNORE INTO associations
									(agg_kind,asc_name,class_name_a,class_name_b,lower_a,upper_a,lower_b,upper_b) 
									VALUES ('none','{asc_name}','{class_a}','{class_b}','{low_a}','{up_a}','{low_b}','{up_b}')""")
		return sql_statements

