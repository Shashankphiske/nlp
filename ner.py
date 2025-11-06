import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Input text
piano_class_text = (
    "Great Piano Academy is situated "
    "in Mayfair or the City of London and has "
    "world-class piano instructors."
)

# Process the text
piano_class_doc = nlp(piano_class_text)

# Print recognized named entities
for ent in piano_class_doc.ents:
    print(
        f"""
ent.text = '{ent.text}'
ent.start_char = {ent.start_char}
ent.end_char = {ent.end_char}
ent.label_ = '{ent.label_}'
spacy.explain('{ent.label_}') = {spacy.explain(ent.label_)}
"""
    )
