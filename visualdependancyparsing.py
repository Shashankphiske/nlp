# ---- Dependency Parsing using spaCy ----
import spacy
from spacy import displacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# Input text
text = "The quick brown fox jumps over the lazy dog."

# Process text
doc = nlp(text)

# Print dependency relations
print("Word\tPOS\tDependency\tHead Word")
for token in doc:
    print(f"{token.text}\t{token.pos_}\t{token.dep_}\t{token.head.text}")

# Visualize (opens in browser)
displacy.serve(doc, style="dep")
