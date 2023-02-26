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
		return lines_attr, lines_noattr

	def filter_gen_comp(self,lines_noattr):
		return lines_gen, lines_comp, lines_noattr_nogencomp

	def filter_active_passive(self,lines_noattr_nogencomp):
		return lines_act, lines_pass, lines_rest




	def filter_nl(self,raw_lines):
		return lines_attr,lines_gen,lines_comp,lines_act,lines_pass,lines_rest 
