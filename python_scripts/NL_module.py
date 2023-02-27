# NL-Filter

################################## Import #################################
# Import libraries:
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
		return

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
					lines_attr.append(line)
					break
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
			else:
				lines_noattr_nogencomp.append(line)
		# Separate Gen from Comp:
		lines_gen = []
		lines_comp = []
		for line in lines_gen_comp:
			for token in line:
				if token.tag_ == "IN":
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
	"""docstring for"""

	def __init__(self):
		self.__sql_ins_class = """INSERT OR IGNORE INTO classes(
									class_name) VALUES"""
		self.__sql_ins_attr = """INSERT OR IGNORE INTO attributes(
									attr_name,class_name) VALUES"""
		self.__sql_ins_gen = """INSERT OR IGNORE INTO associations
									(asc_name,asc_type,class_a,class_b) 
									VALUES ('inherits','generalization',"""
		self.__sql_ins_comp = """INSERT OR IGNORE INTO associations
									(asc_name,asc_type,
										mult_a_1,mult_a_2,mult_b_1,mult_b_2,
										class_a,class_b) 
									VALUES ('is part of','composition',
										'0','*','1','1',"""
		self.__sql_ins_act_asc = """INSERT OR IGNORE INTO associations
									(asc_type,asc_name,class_a, class_b) 
									VALUES ('association',"""
		self.__sql_ins_op = """INSERT OR IGNORE INTO operations(op_name,
									class_name,class_b) VALUES """


	def __get_compound_class_name(self,token):
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
		if token.lemma_.lower() not in class_name.lower():
			if token.text.isupper() is False:
				class_name = token.lemma_.capitalize()
			else:
				class_name = token.lemma_.upper()
		return class_name

	def attr_to_sql (self, lines_attr):
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
			for token in line:
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
		sql_queue = []
		for line in lines_gen:
			child = ""
			parent = ""
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						child = self.__get_compound_class_name(token)
					if "attr" in token.head.dep_:
						parent = self.__get_compound_class_name(token)
			for token in line:
				if "subj" in token.dep_:
					child = self.__get_class_name(token,child)
				if "attr" in token.dep_:
					parent = self.__get_class_name(token,parent)
			sql_queue.extend((
				f"{self.__sql_ins_class} ('{child}'),('{parent}')",
				f"{self.__sql_ins_gen}'{child}','{parent}')"))
		return sql_queue

	def comp_to_sql (self,lines_comp):
		sql_queue = []
		for line in lines_comp:
			child = ""
			parent = ""
			for token in line:
				if token.dep_ == "compound":
					if "subj" in token.head.dep_:
						child = self.__get_compound_class_name(token)
					if "obj" in token.head.dep_:
						parent = self.__get_compound_class_name(token)
			for token in line:
				if "subj" in token.dep_:
					child = self.__get_class_name(token,child)
				if "obj" in token.dep_:
					parent = self.__get_class_name(token,parent)
			sql_queue.extend((
				f"{self.__sql_ins_class} ('{child}'),('{parent}')",
				f"{self.__sql_ins_comp}'{child}','{parent}')"))
		return sql_queue
 
	def act_asc_to_sql (self,lines_act):
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
						mult_pass = ["1","1"]
			op_name = asc_name + pass_class + "()"

			sql_queue.extend((
				f"{self.__sql_ins_class} ('{act_class}'),('{pass_class}')",

				f"""{self.__sql_ins_act_asc} '{asc_name}','{act_class}',
				'{pass_class}')""",

				f"""UPDATE associations SET mult_b_1 = '{mult_pass[0]}',
				mult_b_2 = '{mult_pass[1]}' WHERE asc_name = '{asc_name}' AND
				class_a = '{act_class}' AND class_b = '{pass_class}'""",

				f"""{self.__sql_ins_op} ('{op_name}','{act_class}',
				'{pass_class}')"""))

		return sql_queue

	def pass_acc_to_sql (self,lines_pass):
		pass 

	def transform_nl_sql (self,lines_attr=None,lines_gen=None,lines_comp=None,
		lines_act=None,lines_pass=None):
		pass







class SQL_NL_Transformer():
	"""docstring for SQL_NL_Transformer"""
	def __init__(self, ):
		#self.arg = arg
		pass