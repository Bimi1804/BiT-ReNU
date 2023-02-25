# Database-Handler for BiT-ReNU

# Import libraries:
import sqlite3 
import os
import pandas as pd


# Database Handler class:
class DB_Handler:
	"""
	Manages the database connection.

	Attributes
	----------
	curr_project : str
		The current active project.

	Methods
	-------
	connect_to_db(path) : sqlite3.cursor, sqlite3.connection
		Connect to DB with defined settings.
	create_new_project(project_name) : bool
		Create a new database file with the needed db-structure.
	set_curr_project(project_name) : bool
		Saves the path of an existing project as the current project.
	write_to_db(sql_statement) : bool
		Write to the current database.
	read_all_db() : list of pandas.Dataframe
		Read the whole database into pandas dataframes.

	"""

	def __init__(self):
		self.curr_project = None

	def connect_to_db(self,db_path=None):
		"""
		Connect to database with defined settings.

		Parameters
		----------
		path : str
			The path of a database file.

		Returns
		-------
		curs : sqlite3.cursor
			The sqlite cursor object for the database.
		conn : sqlite3.connection
			The sqlite connection object for the database.
		"""
		if db_path is None:
			db_path = self.curr_project
		conn = sqlite3.connect(db_path)
		curs = conn.cursor()
		# Enable foreign keys:
		curs.execute("""PRAGMA foreign_keys = 1""")
		return curs,conn

	def create_new_project(self, project_name):
		"""
		Create a new database file and create the database structure.

		Parameters
		---------
		project_name : str
			The name of the new project.

		Returns
		-------
		True -> The new database was created successfully.
		False -> The database already exists.

		"""
		# Check if project already exists:
		db_path = os.path.dirname(os.getcwd())+"\\project_databases\\"+ project_name +".db"
		if os.path.isfile(db_path) is True:
			print("Project already exists!")
			return False

		# Connect to DB:
		curs,conn = self.connect_to_db(db_path)

		# Create DB-structure:
		curs.execute("""CREATE TABLE requirements
						(req_id VARCHAR PRIMARY KEY)""")
		curs.execute("""CREATE TABLE classes
						(class_name VARCHAR PRIMARY KEY)""")
		curs.execute("""CREATE TABLE req_and_classes
						(req_id VARCHAR,
						class_name VARCHAR,
						FOREIGN KEY(req_id) REFERENCES requirements(req_id),
						FOREIGN KEY(class_name) REFERENCES classes(class_name))
						""")
		curs.execute("""CREATE TABLE attributes
						(attr_id VARCHAR PRIMARY KEY,
						attr_name VARCHAR, 
						class_name VARCHAR,
						req_id VARCHAR, 
						FOREIGN KEY(class_name) REFERENCES classes(class_name),
						FOREIGN KEY(req_id) REFERENCES requirements(req_id))
						""")
		curs.execute("""CREATE TABLE opperations
						(opp_id VARCHAR PRIMARY KEY,
						opp_name VARCHAR,
						class_name VARCHAR,
						req_id VARCHAR,
						FOREIGN KEY(class_name) REFERENCES classes(class_name),
						FOREIGN KEY(req_id) REFERENCES requirements(req_id))
						""")
		curs.execute("""CREATE TABLE associations
						(asc_id VARCHAR PRIMARY KEY,
						asc_name VARCHAR,
						asc_type VARCHAR,
						req_id VARCHAR,
						class_a VARCHAR,
						class_b VARCHAR,
						mult_a_1 VARCHAR,
						mult_a_2 VARCHAR,
						mult_b_1 VARCHAR,
						mult_b_2 VARCHAR,
						FOREIGN KEY(req_id) REFERENCES requirements(req_id),
						FOREIGN KEY(class_a) REFERENCES classes(class_name),
						FOREIGN KEY(class_b) REFERENCES classes(class_name))
						""")
		conn.commit()
		conn.close()
		return True

	def set_curr_project(self,project_name):
		"""
		Set path of current project.

		Parameters
		----------
		project_name : str
			Name of an existing project.

		Returns
		-------
		True -> Project exists
		False -> Project does not exist
		"""
		db_path = os.path.dirname(os.getcwd())+"\\project_databases\\"+ project_name +".db"
		if os.path.isfile(db_path) is False:
			print("Project does not exist!")
			return False
		else:
			self.curr_project = db_path
			return True

	def write_to_db(self,sql_statements):
		"""
		Writes to the current project.

		Parameters
		----------
		sql_statement : list of str
			A list of all sql statements that should be executed.

		Returns
		-------
		True -> All Statements were executed successfully.
		False -> No active project is selected.
		"""
		if self.curr_project is None:
			print("No active project selected!")
			return False
		# Connect to active project
		curs,conn = self.connect_to_db()
		for statement in sql_statements:
			curs.execute(statement)
		conn.commit()
		conn.close()
		return True

	def read_all_db(self):
		"""
		Read the whole database.

		Parameters
		----------
		None

		Returns
		-------
		df_req : pandas.DataFrame
			The requirements table
		df_class : pandas.DataFrame
			The classes table
		df_re_and_class : pandas.DataFrame
			The requirements_and_classes table
		df_attr : pandas.DataFrame
			The attribute table
		df_opp : pandas.DataFrame
			The opperations table
		df_asc : pandas.DataFrame
			The associations table

		"""
		if self.curr_project is None:
			print("No active project selected!")
			return False
		curs,conn = self.connect_to_db()
		# Read requirements table:----------------------------------------
		curs.execute("""
			SELECT * FROM requirements
			""")
		df_req = pd.DataFrame(curs.fetchall(),columns=["req_id"])
		# Read classes tables:--------------------------------------------
		curs.execute("""
			SELECT * FROM classes
			""")
		df_class = pd.DataFrame(curs.fetchall(),columns=["class_name"])
		# Read requirements_and_clases table:------------------------------
		curs.execute("""
			SELECT * FROM req_and_classes
			""")
		df_re_and_class = pd.DataFrame(curs.fetchall(),columns=["req_id", "class_name"])
		# Read attributes table:-------------------------------------------
		curs.execute("""
			SELECT * FROM attributes
			""")
		df_attr = pd.DataFrame(
							curs.fetchall(),
							columns=["attr_id","attr_name","class", "req_id"])
		# Read ooperations table:------------------------------------------
		curs.execute("""
			SELECT * FROM opperations
			""")
		df_opp = pd.DataFrame(
							curs.fetchall(),
							columns=["opp_id","opp_name","class","req_id"])
		# Read associations table:-----------------------------------------
		curs.execute("""
			SELECT * FROM associations
			""")
		df_asc = pd.DataFrame(
							curs.fetchall(),
							columns=["asc_id", "asc_name", "asc_type",
							"req_id", "class_a", "class_b", "mult_a_1",
							"mult_a_2", "mult_b_1", "mult_b_2"])
		conn.close()
		return df_req,df_class,df_re_and_class,df_attr,df_opp,df_asc

#-----------------------------------------------------------



def test_function():
	#---- Test_2-----
	print("TEST 2:-----------------")
	print("")

	#----Test-Setup----#
	#Delete previous db:
	test2_db = "test2_db"
	db_path = os.path.dirname(os.getcwd())+"\\project_databases\\"+ test2_db +".db"
	if os.path.isfile(db_path):
		os.remove(db_path)
	#---------------#

	test2 = DB_Handler()
	test2.create_new_project(test2_db)
	test2.set_curr_project(test2_db)

	req1 = ["""INSERT INTO classes (class_name) VALUES("user"),("report")""",
			"""INSERT INTO requirements (req_id) VALUES("req.1")""",
			"""INSERT INTO req_and_classes (req_id,class_name) 
				VALUES("req.1","user"),("req.1","report")""",
			"""INSERT INTO associations (asc_id,asc_name,asc_type,
				req_id,class_a,class_b) VALUES ("asc.1","create","basic",
				"req.1","user","report")""",
			"""INSERT INTO opperations (opp_id,opp_name,class_name,req_id) VALUES (
				"opp.1","create","user","req.1")"""]

	test2.write_to_db(req1)

	for df in test2.read_all_db():
		print(df)
		print("")
	return


#test_function()