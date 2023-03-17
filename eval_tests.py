# Evaluation Tests:

# Setup:
from python_scripts.DB_module import *
from python_scripts.NL_module import *
from python_scripts.UML_module import *

# DB-Module:
db_mod = DB_Handler()

# NL-Modules:
nl_filter = NL_Filter()
nl_sql = NL_SQL_Transformer()
sql_nl = SQL_NL_Transformer()

# UML-Modules:
sql_uml = SQL_UML_Transformer()
uml_sql = UML_SQL_Transformer()


# 01:
# NL -> UML -------------------------------------------------

# create new project and connect:
db_mod.create_new_project("test_01")
db_mod.set_curr_project("test_01")

# Import NL:
with open(os.getcwd()+"\\test_cases\\test_requirements_NL.txt") as file:
	lines = file.readlines()
	lines_clean = []
	for l in lines:
		l = l.replace("\n","")
		lines_clean.append(l)

# Filter NL:	
filtered_nl = nl_filter.filter_nl(lines_clean)

# NL -> DB:
sql_queues = nl_sql.transform_nl_sql(filtered_nl)
db_mod.write_to_db(sql_queues)

# DB -> UML:
dataframes = db_mod.read_all_db()
plant_dia = sql_uml.sql_to_plantuml(dataframes)
print(plant_dia)

# Clean-Up:
db_mod.delete_db_file("test_01")

# 01.1:---------------------------------------------------------
# NL -> UML (change element) -> NL

# 01.2:
# NL -> UML (add element) -> NL

#01.3:
# NL -> UML (delete element) -> NL
