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
				2 = operations table
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
		sql_statemens : list(str)
			List of SQL-statements.
		"""

		plant_txt = plant_txt.replace(" ","")
		#-------------------------
		sql_statemens = []
		while "class" in plant_txt:
			class_start = plant_txt.find("class")
			class_content_start = plant_txt.find("{")
			class_content_end = plant_txt.find("}")
			class_name = plant_txt[class_start+5:class_content_start]
			class_content = plant_txt[class_content_start+1:class_content_end].replace("\n","")
			plant_txt = plant_txt[class_content_end+1:]
			class_attr = []
			class_op = []
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
				if "()" in item:
					class_op.append(item)
				if "()" not in item:
					class_attr.append(item)
			sql_statemens.append(f"""INSERT OR IGNORE INTO classes(class_name) VALUES ('{class_name.replace(" ","")}')""")
			for attr in class_attr:
				if attr != "":
					sql_statemens.append(f"""INSERT OR IGNORE INTO attributes(attr_name,class_name) VALUES ('{attr.replace(" ","")}','{class_name.replace(" ","")}')""")
			op_name_class_b = []
			for op in class_op:
				upper = []
				for i in range(len(op)):
					if op[i].isupper() is True:
						upper.append(i)
				op_name = op[:upper[0]]
				op_class_b = op[upper[0]:].replace("()","")
				sql_statemens.append(f"""INSERT OR IGNORE INTO classes(class_name) VALUES ('{op_class_b.replace(" ","")}')""")
				sql_statemens.append(f"""INSERT OR IGNORE INTO operations(op_name,class_name,class_b) 
					VALUES ('{op}','{class_name.replace(" ","")}','{op_class_b.replace(" ","")}')""")


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
			sql_statemens.append(f"""INSERT OR IGNORE INTO associations(asc_name,asc_type,class_a,class_b) 
											VALUES ('inherits','generalization', '{gen[arrow+4:]}','{gen[:arrow]}')""")

		for comp in composition:
			arrow = comp.find("*--")
			sql_statemens.append(f"""INSERT OR IGNORE INTO associations(asc_name,asc_type,
									mult_a_1,mult_a_2,mult_b_1,mult_b_2,class_a,class_b) 
									VALUES ('is part of','composition','0','*','1','1',
									'{comp[arrow+3:]}','{comp[:arrow]}')""")
		plant_asc_lines = plant_txt.splitlines()
		associations = []
		for line in plant_asc_lines:
			if line != "" and line != "@enduml":
				associations.append(line)
		for line in associations:
			pointer = line.find('"')
			class_a = line[:pointer]
			line = line[pointer:]
			pointer = line.find("..")
			mult_a_1 = line[:pointer].replace('"',"")
			line = line[pointer+2:]
			pointer = line.find('"')
			mult_a_2 = line[:pointer].replace('"',"")
			line = line[pointer+1:]
			line = line[line.find('"')+1:]
			pointer = line.find("..")
			mult_b_1 = line[:pointer]
			line = line[pointer:]
			pointer = line.find('"')
			mult_b_2 = line[:pointer].replace("..","")
			line = line[pointer+1:]
			pointer = line.find(":")
			class_b = line[:pointer]
			asc_name = line[pointer+1:]
			sql_statemens.append(f"""INSERT OR IGNORE INTO associations
									(asc_type,asc_name,class_a,class_b,mult_a_1,mult_a_2,mult_b_1,mult_b_2) 
									VALUES ('association','{asc_name}','{class_a}','{class_b}','{mult_a_1}','{mult_a_2}','{mult_b_1}','{mult_b_2}')""")
		return sql_statemens

