# NL-Filter


################################## Import #################################
# Import libraries:
import spacy
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")



################################## Classes #################################

class NL_Filter():
	"""docstring for NL_Filter"""

	def __init__(self):
		#self.arg = arg
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
		
		"""
		lines_nopunctdet = self.rmv_det_punct(raw_lines)
		lines_attr,lines_noattr = self.filter_attr(lines_nopunctdet)
		lines_gen,lines_comp,lines_noattr_nogencomp=self.filter_gen_comp(
			lines_noattr)
		lines_act, lines_pass=self.filter_active_passive(lines_noattr_nogencomp)
		output = [lines_attr,lines_gen,lines_comp,lines_act,lines_pass ]
		return output
