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


db_mod.set_curr_project("test_req1")


dataframes = db_mod.read_all_db()
print(SQL_UML_transformer.sql_to_plantuml(dataframes))



