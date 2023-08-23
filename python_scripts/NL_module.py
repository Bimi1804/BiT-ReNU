# NL-Filter

################################## Import #################################
# Import libraries:
import re

from lemminflect import getInflection # for Verbs
import inflect  # for nouns
inf = inflect.engine()

import spacy
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")

################################## Classes #################################

class NL_Filter():
	"""
	Filters natural language into sentences that contain certain UML 
	elements.

	Methods
	-------
	rmv_det_punct(list(str)) : list(spacy.doc)
		Removes determiners (DET) and punctuation (PUNCT).
	filter_attr(list(spacy.doc)) : list(spacy.doc),list(spacy.doc)
		Filter sentences that contain attributes.
	filter_gen_comp(list(spacy.doc)) : list(spacy.doc),list(spacy.doc),list(spacy.doc)
		Filters sentences that contain generalization or composition.
	filter_active_passive(list(spacy.doc)) : list(spacy.doc),list(spacy.doc)
		Filter active associations and passive associations.
	filter_nl(list(str)) : list(list(spacy.doc))
		Filters a list of sentences into sentences with UML elements.
	"""

	def __init__(self):
		pass

	def rmv_det_punct(self,lines):
		"""
		Removes determiners (DET) and punctuation (PUNCT).

		Parameters
		----------
		lines: list(str)
			A list of sentences. Each element is a sentence as a string

		Returns
		-------
		lines_nopunctdet: list(spacy.doc)
			A list, where each element is a list of tokens of the raw
			sentences. Without the DET and PUNCT tokens.
		"""
		lines_nopunctdet = []
		for line in lines:
			doc = nlp(line)
			line = []
			for token in doc:
				if token.pos_ != "DET" and token.pos_ != "PUNCT":
					line.append(token)
			lines_nopunctdet.append(line)
		return lines_nopunctdet 

	def filter_attr(self,lines_nopunctdet):
		"""
		Filter sentences that contain attributes.

		Parameters
		----------
		lines_nopunctdet : list(spacy.doc)
			List of spacy.doc objects that do not contain DET and PUNCT.

		Returns
		-------
		lines_attr : list(spacy.doc)
			List of spacy.doc objects that have attributes.
		lines_noattr : list(spacy.doc)
			List of spacy.doc objects that do not contain attributes.
		"""
		lines_attr = []
		lines_noattr = []
		for line in lines_nopunctdet:
			for token in line:
				if token.lemma_ == "have":
					if previous_token.lemma_ != "must" and previous_token.lemma_ != "can":
						lines_attr.append(line)
						break
				previous_token = token
			else:
				lines_noattr.append(line)
		return lines_attr, lines_noattr

	def filter_gen_comp(self,lines_noattr):
		"""
		Filters sentences that contain generalization or composition.

		Parameters
		----------
		lines_noattr : list(spacy.doc)
			List of spacy.doc objects that do not contain attributes.

		Returns
		-------
		lines_gen : list(spacy.doc)
			List of spacy.doc objects that contain generalizations.
		lines_comp : list(spacy.doc)
			List of spacy.doc objects that contain compositions.
		lines_noattr_nogencomp : list(spacy.doc)
			List of spacy.doc objects that do not contain attributes,
			generalizations, and compositions.
		"""
		# Separate gen and comp from the rest:
		lines_gen_comp = []
		lines_noattr_nogencomp = []
		for line in lines_noattr:
			for token in line:
				if token.dep_ == "ROOT":
					if token.lemma_ == "be":
						lines_gen_comp.append(line)
						break
				if token.lemma_ == "have":
					lines_gen_comp.append(line)
					break
			else:
				lines_noattr_nogencomp.append(line)

		# Separate Gen from Comp:
		lines_gen = []
		lines_comp = []
		for line in lines_gen_comp:
			for token in line:
				if token.tag_ == "IN" or token.lemma_ == "have":
					lines_comp.append(line)
					break
			else:
				lines_gen.append(line)
		return lines_gen, lines_comp, lines_noattr_nogencomp

	def filter_active_passive(self,lines_noattr_nogencomp):
		"""
		Filter active associations and passive associations.

		Parameters
		----------
		lines_noattr_nogencomp : list(spacy.doc)
			List of spacy.doc objects that do not contain attributes,
			generalizations, and compositions.

		Returns
		-------
		lines_act : list(spacy.doc)
			List of spacy.doc objects that contain an active association.
		lines_pass : list(spacy.doc)
			List of spacy.doc objects that contain a passive association.
		"""
		lines_act = []
		lines_pass = []
		for line in lines_noattr_nogencomp:
			for token in line:
				if token.dep_ == "nsubjpass":
					lines_pass.append(line)
					break
			else:
				lines_act.append(line)
		return lines_act, lines_pass

	def filter_nl(self,raw_lines):
		"""
		Filters a list of sentences into sentences with:
			attributes, 
			generalization,
			composition,
			active associations,
			passive associations.

		Parameters
		----------
		raw_lines : list(str)
			A list of sentences. Each element is a sentence as a string

		Returns
		-------
		output : list
			Each element is a list of spacy.doc objects:
			lines_attr : list(spacy.doc)
				List of spacy.doc objects that have attributes.
			lines_gen : list(spacy.doc)
				List of spacy.doc objects that contain generalizations.
			lines_comp : list(spacy.doc)
				List of spacy.doc objects that contain compositions.
			lines_act : list(spacy.doc)
				List of spacy.doc objects that contain an active 
				association.
			lines_pass : list(spacy.doc)
				List of spacy.doc objects that contain a passive 
				association.
		"""
		lines_nopunctdet = self.rmv_det_punct(raw_lines)
		lines_attr,lines_noattr = self.filter_attr(lines_nopunctdet)
		lines_gen,lines_comp,lines_noattr_nogencomp=self.filter_gen_comp(
			lines_noattr)
		lines_act, lines_pass=self.filter_active_passive(lines_noattr_nogencomp)
		output = [lines_attr,lines_gen,lines_comp,lines_act,lines_pass]
		return output

class NL_SQL_Transformer():
	"""
	Holds the functions to transform filtered NL sentences into sql statements.

	Attributes
	----------
	__sql_ins_class : str
		Static part of the sql statement to insert classes.
	__sql_ins_attr : str
		Static part of the sql statement to insert attributes.
	__sql_ins_gen : str
		Static part of the sql statement to insert generalizations.
	__sql_ins_comp : str
		Static part of the sql statement to insert compositions.
	__sql_ins_act_asc : str
		Static part of the sql statement to insert active associations.
	__sql_ins_op : str
		Static part of the sql statement to insert operations.


	Methods
	-------
	__get_compound_class_name(spacy.doc) : str
		Combine compound words and their head to a single class-name-string.
	__get_class_name(spacy.doc, str) : str
		Transform a single spacy.doc object into a class-name-string.
	attr_to_sql ( list(list(spacy.doc))) : list(str)
		Creates sql-statements from a list of tokenized attribute-sentences.
	gen_to_sql ( list(list(spacy.doc))) : list(str)
		Creates sql-statements from a list of tokenized 
		generalization-sentences.
	comp_to_sql (list(list(spacy.doc))) : list(str)
		Creates sql-statements from a list of tokenized composition-sentences.
	act_asc_to_sql (list(list(spacy.doc))) : list(str)
		Creates sql-statements from a list of tokenized active 
		association-sentences.
	pass_asc_to_sql (list(list(spacy.doc))) : list(str)
		Creates sql-statements from a list of tokenized passive 
		association-sentences.
	transform_nl_sql (list(list(spacy.doc)),list(list(spacy.doc)),
					  list(list(spacy.doc)),list(list(spacy.doc)),
					  list(list(spacy.doc))) 
					  : list(str)
		Uses all other X_to_sql methods to create sql-statements for 
		everything.
	"""

	def __init__(self):
		self.__sql_ins_class = """INSERT OR IGNORE INTO classes(
									class_name) VALUES"""

		self.__sql_ins_attr = """INSERT OR IGNORE INTO attributes(
									attr_name,class_name) VALUES"""

		self.__sql_ins_gen = """INSERT OR IGNORE INTO generalizations
									(super_class, sub_class) 
									VALUES"""

		self.__sql_ins_comp = """INSERT OR IGNORE INTO associations
									(agg_kind,asc_name,lower_a,upper_a,class_name_a,class_name_b) 
									VALUES ('composite','is part of','1','*',"""

		self.__sql_ins_act_asc = """INSERT OR IGNORE INTO associations
									(agg_kind,asc_name,class_name_a, class_name_b) 
									VALUES ('none',"""

	def __get_compound_class_name(self,token):
		"""
		Combine compound words and their head to a single class-name-string.

		Parameters
		----------
		token : spacy.doc
			A token of a sentence as a spacy.doc object.

		Returns
		-------
		class_name : str
			A single string in the format of a class name.

		"""
		if token.text.isupper() is False:
			class_name = token.lemma_.capitalize()
		else:
			class_name = token.lemma_.upper()
		if token.head.text.isupper() is False:
			class_name = class_name + token.head.lemma_.capitalize()
		else:
			class_name = class_name + token.head.lemma_.upper()
		return class_name

	def __get_class_name(self,token,class_name):
		"""
		Transform a single spacy.doc object into a class-name-string.

		Parameters
		----------
		token : spacy.doc
			A token of a sentence as a spacy.doc object.
		class_name : str
			A current class name, that might not be the right class name-

		Returns
		-------
		class_name : str
			A single string in the format of a class name.

		"""
		if token.lemma_.lower() not in class_name.lower():
			if token.text.isupper() is False:
				class_name = token.lemma_.capitalize()
			else:
				class_name = token.lemma_.upper()
		return class_name

	def attr_to_sql (self, lines_attr):
		"""
		Creates sql-statements from a list of tokenized attribute-sentences.

		Parameters
		----------
		lines_attr : list(list(spacy.doc))
			A list of tokenized attribute sentences. The tokens are spacy.doc 
			objects.

		Returns
		-------
		sql_queue : list(str)
			A list of sql statements for the given sentences.

		"""
		sql_queue = []
		for line in lines_attr:
			subj = ""
			attr = ""
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						subj = self.__get_compound_class_name(token)
					if "obj" in token.head.dep_:
						if token.text.isupper() is False:
							attr = token.lemma_.lower()
						else:
							attr = token.lemma_.upper()
						if token.head.text.isupper() is False:
							attr = attr + token.head.lemma_.capitalize()
						else:
							attr = attr + token.head.lemma_.upper()
				if "subj" in token.dep_:
					subj = self.__get_class_name(token,subj)

				if "obj" in token.dep_:
					if token.lemma_.lower() not in attr.lower():
						if token.text.isupper() is False:
							attr = token.lemma_.lower()
						else:
							attr = token.lemma_.upper()
			sql_queue.extend((f"{self.__sql_ins_class} ('{subj}')",
								f"{self.__sql_ins_attr} ('{attr}','{subj}')"))
		return sql_queue
		 
	def gen_to_sql (self, lines_gen):
		"""
		Creates sql-statements from a list of tokenized 
		generalization-sentences.

		Parameters
		----------
		lines_gen : list(list(spacy.doc))
			A list of tokenized generalization sentences. 
			The tokens are spacy.doc objects.

		Returns
		-------
		sql_queue : list(str)
			A list of sql statements for the given sentences.

		"""
		sql_queue = []
		for line in lines_gen:
			parent = ""
			child = ""
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						parent = self.__get_compound_class_name(token)
					if "attr" in token.head.dep_:
						child = self.__get_compound_class_name(token)
				if "subj" in token.dep_:
					parent = self.__get_class_name(token,parent)
				if "attr" in token.dep_:
					child = self.__get_class_name(token,child)
			sql_queue.extend((
				f"{self.__sql_ins_class} ('{child}'),('{parent}')",
				f"{self.__sql_ins_gen}('{parent}','{child}')"))
		return sql_queue

	def comp_to_sql (self,lines_comp):
		"""
		Creates sql-statements from a list of tokenized composition-sentences.

		Parameters
		----------
		lines_comp : list(list(spacy.doc))
			A list of tokenized composition sentences. The tokens are spacy.doc 
			objects.

		Returns
		-------
		sql_queue : list(str)
			A list of sql statements for the given sentences.

		"""

		sql_queue = []
		lines_comp_act = []
		lines_comp_pass = []
		for line in lines_comp:
			for token in line:
				if token.dep_ == "aux":
					lines_comp_pass.append(line)
					break
				lines_comp_act.append(line)
				
		for line in lines_comp_act:
			class_name_a = ""
			class_name_b = ""

			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						class_name_a = self.__get_compound_class_name(token)
					if "obj" in token.head.dep_:
						class_name_b = self.__get_compound_class_name(token)
				if "subj" in token.dep_:
					class_name_a = self.__get_class_name(token,class_name_a)
				if "obj" in token.dep_:
					class_name_b = self.__get_class_name(token,class_name_b)
			sql_queue.extend((
				f"{self.__sql_ins_class} ('{class_name_a}'),('{class_name_b}')",

				f"{self.__sql_ins_comp}'{class_name_a}','{class_name_b}')",

				f"""UPDATE associations SET lower_b = '{mult_comp[0]}',
				upper_b = '{mult_comp[1]}' WHERE asc_name = 'is part of' AND
				class_name_a = '{class_name_a}' AND class_name_b = '{class_name_b}'"""))

###############################################################################################################
# Problem: Multiplicity leer lassen, wenn kein "can|must have" Satz vorhanden ist!
# Dieses Konzept dann überall durchführen -> Auch eine Möglichkeit finden, dass man bei Association keine Multi haben kann wenn ein Satz fehlt.

		for line in lines_comp_pass:
			class_name_a = ""
			class_name_b = ""
			mult_comp = ["0","*"]
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						class_name_b = self.__get_compound_class_name(token)
					if "obj" in token.head.dep_:
						class_name_a = self.__get_compound_class_name(token)
				if "subj" in token.dep_:
					class_name_b = self.__get_class_name(token,class_name_b)
				if "obj" in token.dep_:
					class_name_a = self.__get_class_name(token,class_name_a)
				
				if token.dep_ == "aux":						
					if token.lemma_ == "must":
						mult_comp = ["1","*"]
			sql_queue.extend((
				f"{self.__sql_ins_class} ('{class_name_a}'),('{class_name_b}')",

				f"{self.__sql_ins_comp}'{class_name_a}','{class_name_b}')",

				f"""UPDATE associations SET lower_b = '{mult_comp[0]}',
				upper_b = '{mult_comp[1]}' WHERE asc_name = 'is part of' AND
				class_name_a = '{class_name_a}' AND class_name_b = '{class_name_b}'"""))

		return sql_queue

###############################################################################################################
 
	def act_asc_to_sql (self,lines_act):
		"""
		Creates sql-statements from a list of tokenized active 
		association-sentences.

		Parameters
		----------
		lines_act : list(list(spacy.doc))
			A list of tokenized active association sentences. The tokens are 
			spacy.doc objects.

		Returns
		-------
		sql_queue : list(str)
			A list of sql statements for the given sentences.

		"""

		sql_queue = []
		for line in lines_act:
			act_class = ""
			pass_class = ""
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						act_class = self.__get_compound_class_name(token)
					if "obj" in token.head.dep_:
						pass_class = self.__get_compound_class_name(token)
				if "subj" in token.dep_:
					act_class = self.__get_class_name(token,act_class)
				if "obj" in token.dep_:
					pass_class = self.__get_class_name(token,pass_class)
				if token.dep_ == "ROOT":
					asc_name = token.lemma_
				if token.dep_ == "aux":
					if token.lemma_ == "can":
						mult_pass = ["0","*"]
					if token.lemma_ == "must":
						mult_pass = ["1","*"]

			sql_queue.extend((
				f"{self.__sql_ins_class} ('{act_class}'),('{pass_class}')",

				f"""{self.__sql_ins_act_asc} '{asc_name}','{act_class}',
				'{pass_class}')""",

				f"""UPDATE associations SET lower_b = '{mult_pass[0]}',
				upper_b = '{mult_pass[1]}' WHERE asc_name = '{asc_name}' AND
				class_name_a = '{act_class}' AND class_name_b = '{pass_class}'"""))
		return sql_queue

	def pass_asc_to_sql (self,lines_pass):
		"""
		Creates sql-statements from a list of tokenized passive 
		association-sentences.

		Parameters
		----------
		lines_pass : list(list(spacy.doc))
			A list of tokenized passive association sentences. The tokens are 
			spacy.doc objects.

		Returns
		-------
		sql_queue : list(str)
			A list of sql statements for the given sentences.

		"""

		sql_queue = []
		for line in lines_pass:
			act_class = ""
			pass_class = ""
			asc_name = ""
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						pass_class = self.__get_compound_class_name(token)
					if "obj" in token.head.dep_:
						act_class = self.__get_compound_class_name(token)
				if "subj" in token.dep_:
					pass_class = self.__get_class_name(token,pass_class)
				if "obj" in token.dep_:
					act_class = self.__get_class_name(token,act_class)
				if token.dep_ == "ROOT":
					asc_name = token.lemma_
				if token.dep_ == "aux":
					if token.lemma_ == "can":
						mult_act = ["0","*"]
					if token.lemma_ == "must":
						mult_act = ["1","1"]
			sql_queue.extend((
				f"{self.__sql_ins_class} ('{act_class}'),('{pass_class}')",

				f"""{self.__sql_ins_act_asc} '{asc_name}','{act_class}',
				'{pass_class}')""",

				f"""UPDATE associations SET lower_a = '{mult_act[0]}',
				upper_a = '{mult_act[1]}' WHERE asc_name = '{asc_name}' AND
				class_name_a = '{act_class}' AND class_name_b = '{pass_class}'"""))

		return sql_queue

	def transform_nl_sql (self,output=[],lines_attr=[],lines_gen=[],lines_comp=[],
		lines_act=[],lines_pass=[]):
		"""
		Uses all other X_to_sql methods to create sql-statements for 
		everything.

		Parameters
		----------
		lines_attr : list(list(spacy.doc))
			A list of tokenized attribute sentences. The tokens are spacy.doc 
			objects.
		lines_gen : list(list(spacy.doc))
			A list of tokenized generalization sentences. The tokens are 
			spacy.doc objects.
		lines_comp : list(list(spacy.doc))
			A list of tokenized composition sentences. The tokens are spacy.doc 
			objects.
		lines_act : list(list(spacy.doc))
			A list of tokenized active association sentences. The tokens are 
			spacy.doc objects.
		lines_pass : list(list(spacy.doc))
			A list of tokenized passive association sentences. The tokens are 
			spacy.doc objects.

		Returns
		-------
		sql_queue : list(str)
			A list of sql statements for the given sentences.
		"""
		if output != []:
			lines_attr = output[0]
			lines_gen = output[1]
			lines_comp = output[2]
			lines_act = output[3]
			lines_pass = output[4]
		sql_queue = []
		for statement in self.attr_to_sql(lines_attr):
			sql_queue.append(statement)
		for statement in self.gen_to_sql(lines_gen):
			sql_queue.append(statement)
		for statement in self.comp_to_sql(lines_comp):
			sql_queue.append(statement)
		for statement in self.act_asc_to_sql(lines_act):
			sql_queue.append(statement)
		for statement in self.pass_asc_to_sql(lines_pass):
			sql_queue.append(statement)
		return sql_queue

class SQL_NL_Transformer():
	"""
	Holds the functions to transform pandas dataframes into sentences.

	Methods
	-------
	__separate_noun(str) : str
		Separates concatenated class or attribute names.
	attr_to_nl(pandas.DataFrame) : list(str)
		Creates sentences from the attributes table.
	asc_to_nl(pandas.DataFrame) : list(str),list(str),list(str)
		Creates sentences from the association table.
	transform_sql_nl(list(pandas.Dataframe)) : list(str)
		Transform dataframes into sentences.
	"""
	def __init__(self, ):
		pass

	def __separate_noun(self, noun):
		"""
		Separates concatenated class or attribute names.

		Parameters
		----------
		noun : str
			A class or attribute name

		Returns
		-------
		noun : str
			The given class or attribute name. If the name was a combination of
			multiple words, the returned string contains the single words 
			separated by " ".
		"""
		up_count = sum(1 for letter in noun if letter.isupper())
		if up_count < 2:
			noun = noun.lower()
		if up_count > 1:
			noun_parts = re.findall('[A-Z][^A-Z]*',noun)
			noun = ""
			for word in noun_parts:
				if noun == "":
					noun = word.lower()
				elif noun != "":
					noun = f"{noun} {word.lower()}"
		return noun

	def attr_to_nl(self,attr_df):
		"""
		Creates sentences from the attributes table.

		Parameters
		----------
		attr_df : pandas.DataFrame
			The attribute table from the sql database as a pandas Dataframe.

		Returns
		-------
		attr_sentences : list(str)
			A list of the generated sentences.
		"""
		attr_sentences = []
		for index, row in attr_df.iterrows():
			subj =""
			obj = ""
			if row[1].isupper() is True:
				subj = row[1]
			if row[1].isupper() is False:
				up_count = sum(1 for letter in row[1] if letter.isupper())
				if up_count < 2:
					subj = row[1].lower()
				if up_count > 1:
					subj_parts = re.findall('[A-Z][^A-Z]*',row[1])
					for word in subj_parts:
						if subj == "":
							subj = word.lower()
						elif subj != "":
							subj = f"{subj} {word.lower()}"
			if row[0].isupper() is True:
				obj = row[0]
			if row[0].isupper() is False:
				up_count = sum(1 for letter in row[0] if letter.isupper()) 
				if up_count == 0:
					obj = row[0]
				upper_ind = []
				for index in range(len(row[0])):
					if row[0][index].isupper() is True:
						upper_ind.append(index)
				if upper_ind != []:
					for i in range(len(upper_ind)):
						if i == 0:
							obj = row[0][0:upper_ind[i]].lower()
						if i < len(upper_ind)-1:
							obj = f"{obj} {row[0][upper_ind[i]:upper_ind[i]+1].lower()}"
						if i == len(upper_ind)-1:
							obj = f"{obj} {row[0][upper_ind[i]:].lower()}"
			attr_sentences.append((f"{inf.a(subj)} has {inf.a(obj)}.").capitalize())
		return attr_sentences

	def gen_to_nl(self,gen_df):
		gen_sent = []
		for index, row in gen_df.iterrows():
			subj = row[0]
			obj = row[1]
			if subj.isupper() is False:
				subj = self.__separate_noun(subj)
			if obj.isupper() is False:
				obj = self.__separate_noun(obj)
			gen_sent.append((f"{inf.a(subj)} is {inf.a(obj)}.").capitalize())
		return gen_sent

	def asc_to_nl(self,asc_df):
		"""
		Creates sentences from the association table.

		Parameters
		----------
		asc_df : pandas.DataFrame
			The association table from the sql database as a pandas Dataframe.

		Returns
		-------
		gen_sent : list(str)
			A list of the generated generalization sentences.
		comp_sent : list(str)
			A list of the generated composition sentences
		asc_sent : list(list(str))
			A list of the generated association sentences. Each inner list 
			contains two elements: 
				[0] = Active sentence
				[1] = Passive sentence
		"""

		comp_sent = []
		asc_sent = []
		for index, row in asc_df.iterrows():
			asc_type = row[1]
			subj = row[2]
			obj = row[3]
			verb = row[0]
			mult_subj = row[6]
			mult_obj = row[4]
			if subj.isupper() is False:
				subj = self.__separate_noun(subj)
			if obj.isupper() is False:
				obj = self.__separate_noun(obj)
			# Composition
			if asc_type == "composite":
				comp_sent.append((f"{inf.a(obj)} is part of {inf.a(subj)}.").capitalize())
				modal_comp = "can"
				if mult_subj == "1":
					modal_comp = "must"
				comp_sent.append((f"{inf.a(subj)} {modal_comp} have {inf.a(obj)}.").capitalize())
			# Active/Passive Association
			if asc_type == "none":
				if mult_subj == "0":
					modal_act = "can"
				if mult_subj == "1":
					modal_act = "must"
				if mult_obj == "0":
					modal_pass = "can"
				if mult_obj == "1":
					modal_pass = "must"
				verb_pass = getInflection(verb,tag="VBD")
				asc_sent.append([(f"""{inf.a(subj)} {modal_act} {verb} {inf.a(obj)}.""").capitalize(),
								(f"""{inf.a(obj)} {modal_pass} be {verb_pass[0]} by {inf.a(subj)}.""").capitalize()])
		return comp_sent, asc_sent

	def transform_sql_nl(self,dataframes):
		"""
		Transform dataframes into sentences.

		Parameters
		----------
		dataframes : list(pandas.DataFrame)
			List with dataframes of the DB-tables. Elements of the list have to
			be in the following order:
				0 = classes table
				1 = attributes table
				2 = generalization table
				3 = associations table

		Returns
		-------
		sentences : list(str)
			List with sentences.
		"""
		df_class = dataframes[0]
		df_attr = dataframes[1]
		df_gen = dataframes[2]
		df_asc = dataframes[3]
		attr_sentences = self.attr_to_nl(df_attr)
		comp_sent, asc_sent = self.asc_to_nl(df_asc)
		gen_sent = self.gen_to_nl(df_gen)
		sentences = []
		for sen in attr_sentences:
			sentences.append(sen)
		for sen in gen_sent:
			sentences.append(sen)
		for sen in comp_sent:
			sentences.append(sen)
		for sen_pair in asc_sent:
			for sen in sen_pair:
				sentences.append(sen)
		return sentences
