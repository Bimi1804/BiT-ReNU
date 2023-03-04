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


db_mod.delete_db_file("test_req1")

db_mod.create_new_project("test_req1")
db_mod.set_curr_project("test_req1")


with open(os.getcwd()+"\\test_cases\\plant_test_requirements.txt") as file:
	plantuml = file.read()



#print(db_mod.read_all_db())

#print(plantuml)

classes = []
attributes = []
operations = []
associations = []

while "class" in plantuml:
	class_start = plantuml.find("class")
	class_content_start = plantuml.find("{")
	class_content_end = plantuml.find("}")
	class_name = plantuml[class_start+6:class_content_start]
	class_content = plantuml[class_content_start+1:class_content_end]
	plantuml = plantuml[class_content_end+1:]
	class_attr = []
	class_op = []
	while "+" in class_content:
		attr_op_start = class_content.find("+")
		if "+" in class_content[attr_op_start+2:]:
			attr_op_end = class_content[attr_op_start+1:].find("+")
		else:
			attr_op_end = len(class_content)
		item = class_content[attr_op_start+2:attr_op_end+1]
		item = item.replace("\n","")
		if "()" in item:
			class_op.append(item)
		if "()" not in item:
			class_attr.append(item)
		if "+" in class_content[attr_op_start+2:]:
			class_content = class_content[attr_op_end+2:]
		else:
			class_content = ""
	classes.append(class_name)
	attributes.append([class_name,class_attr])
	op_name_class_b = []
	for op in class_op:
		upper = []
		for i in range(len(op)):
			if op[i].isupper() is True:
				upper.append(i)
		op_name = op[:upper[0]]
		op_class_b = op[upper[0]:].replace("()","")
		op_name_class_b.append([op_name,op_class_b])


	operations.append([class_name,op_name_class_b])

print("CLASSES:")
for i in classes:
	print(i)

print("\nATTRIBUTES:")
for i in attributes:
	if i[1] != []:
		print(f"{i[0]}: {i[1]}")

print("\nOPERATIONS:")
for i in operations:
	if i[1] != []:
		print(f"{i[0]}: {i[1]}")
print("")
#print(plantuml)
generalization = []
composition = []
plant_asc_lines = plantuml.splitlines()
for line in plant_asc_lines:
	if "<|--" in line:
		generalization.append(line)
		plantuml = plantuml.replace(line,"")
	if "*--" in line:
		composition.append(line)
		plantuml = plantuml.replace(line,"")

print("generalization:")
gen = []
for i in generalization:
	arrow = i.find("<|--")
	gen.append([i[:arrow-1],i[arrow+5:]])
for i in gen:
	print(i)


print("\ncomposition:")
comp = []
for i in composition:
	arrow = i.find("*--")
	comp.append([i[:arrow-1],i[arrow+4:]])
for i in comp:
	print(i)



plant_asc_lines = plantuml.splitlines()
associations = []
for line in plant_asc_lines:
	if line != "" and line != "@enduml":
		associations.append(line)

print("\nAssociations:")
for i in associations:
	print(i)
	print(i[i.find('"'):i.find('"')+5])



#print(plantuml[class_content_start+1:class_content_end])





plantuml = plantuml[class_content_end+1:]
#print("-----------------")
#print(plantuml)