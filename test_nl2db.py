# Test interface NL2DB
import os
import pandas as pd

from python_scripts.DB_module import *
from python_scripts.NLP_module import *

db_mod = DB_Handler()
NLP_mod = NLP_Handler()

db_mod.create_new_project("test_req1")
db_mod.set_curr_project("test_req1")










# Read DB
for df in db_mod.read_all_db():
	print(df)
	print("")
