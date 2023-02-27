# Database-Handler for BiT-ReNU

################################## Import #################################
# Import libraries:
import sqlite3 
import os
import pandas as pd


################################## Classes #################################
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
	delete_db_file(str) : 
		Delete a database file.
	"""

	def __init__(self):
		self.curr_project = None
		self.root_folder = os.getcwd()

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
		db_path = self.root_folder+"\\project_databases\\"+ project_name +".db"
		if os.path.isfile(db_path) is True:
			print("Project already exists!")
			return False

		# Connect to DB:
		curs,conn = self.connect_to_db(db_path)

		# Create DB-structure:
		curs.execute("""CREATE TABLE classes
						(class_name VARCHAR NOT NULL PRIMARY KEY)""")
		curs.execute("""CREATE TABLE attributes
						(attr_name VARCHAR NOT NULL, 
						class_name VARCHAR NOT NULL,
						PRIMARY KEY(attr_name,class_name),
						FOREIGN KEY(class_name) REFERENCES classes(class_name))
						""")
		curs.execute("""CREATE TABLE operations
						(op_name VARCHAR NOT NULL,
						class_name VARCHAR NOT NULL,
						class_b VARCHAR,
						PRIMARY KEY(op_name,class_name),
						FOREIGN KEY(class_name) REFERENCES classes(class_name),
						FOREIGN KEY(class_b) REFERENCES classes(class_name),
						""")
		curs.execute("""CREATE TABLE associations
						(asc_name VARCHAR NOT NULL,
						asc_type VARCHAR,
						class_a VARCHAR NOT NULL,
						class_b VARCHAR NOT NULL,
						mult_a_1 VARCHAR,
						mult_a_2 VARCHAR,
						mult_b_1 VARCHAR,
						mult_b_2 VARCHAR,
						PRIMARY KEY(asc_name,class_a,class_b)
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
		db_path = self.root_folder+"\\project_databases\\"+ project_name +".db"
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
			print(statement)
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
		df_class : pandas.DataFrame
			The classes table
		df_attr : pandas.DataFrame
			The attribute table
		df_op : pandas.DataFrame
			The operations table
		df_asc : pandas.DataFrame
			The associations table

		"""
		if self.curr_project is None:
			print("No active project selected!")
			return False
		curs,conn = self.connect_to_db()
		# Read requirements table:----------------------------------------
		# Read classes tables:--------------------------------------------
		curs.execute("""
			SELECT * FROM classes
			""")
		df_class = pd.DataFrame(curs.fetchall(),columns=["class_name"])
		# Read requirements_and_clases table:------------------------------
		# Read attributes table:-------------------------------------------
		curs.execute("""
			SELECT * FROM attributes
			""")
		df_attr = pd.DataFrame(
							curs.fetchall(),
							columns=["attr_name","class_name"])
		# Read operations table:------------------------------------------
		curs.execute("""
			SELECT * FROM operations
			""")
		df_op = pd.DataFrame(
							curs.fetchall(),
							columns=["op_name","class_name","class_b"])
		# Read associations table:-----------------------------------------
		curs.execute("""
			SELECT * FROM associations
			""")
		df_asc = pd.DataFrame(
							curs.fetchall(),
							columns=["asc_name", "asc_type","class_a", 
							"class_b", "mult_a_1","mult_a_2", "mult_b_1", 
							"mult_b_2"])
		conn.close()
		return df_class,df_attr,df_op,df_asc

	def delete_db_file(self, project_name):
		"""
		Delete a database file.

		Parameters
		----------
		project_name : str
			The name of the project that should be deleted.

		Returns
		-------
		None
		"""
		db_path = self.root_folder+"\\project_databases\\"+ project_name +".db"
		os.remove(db_path)
		return 

