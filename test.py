import spacy
# Load the "en_core_web_sm" pipeline
nlp = spacy.load("en_core_web_sm")


test = "A report can be written by a user."

doc = nlp(test)
print(doc)
for token in doc:
	print(f"{token} = {token.dep_}")