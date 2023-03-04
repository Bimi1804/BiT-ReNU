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
	class_name ={plantuml[class_start+6:class_content_start]}
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


print(classes)

print("-------------------")
print(attributes)





#print(plantuml[class_content_start+1:class_content_end])





plantuml = plantuml[class_content_end+1:]
#print("-----------------")
#print(plantuml)