# ---- NLP Text Representation: Bag of Words, TF-IDF, and Word2Vec ----

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk

# Download tokenizer data
nltk.download('punkt')

# ---- Sample Corpus ----
corpus = [
    "The cat sat on the mat",
    "The dog sat on the log",
    "Dogs and cats are friends"
]

# ---------- 1. Bag of Words ----------
vectorizer = CountVectorizer()
X_bow = vectorizer.fit_transform(corpus)
print("---- Bag of Words ----")
print(vectorizer.get_feature_names_out())
print(X_bow.toarray())

# ---------- 2. TF-IDF ----------
tfidf = TfidfVectorizer()
X_tfidf = tfidf.fit_transform(corpus)
print("\n---- TF-IDF ----")
print(tfidf.get_feature_names_out())
print(X_tfidf.toarray())

# ---------- 3. Word2Vec ----------
# Tokenize sentences
tokenized_sentences = [word_tokenize(sent.lower()) for sent in corpus]

# Train Word2Vec model
model = Word2Vec(sentences=tokenized_sentences, vector_size=50, window=3, min_count=1, workers=2)

print("\n---- Word2Vec ----")
print("Vector for 'cat':\n", model.wv['cat'])
print("\nMost similar words to 'cat':")
print(model.wv.most_similar('cat'))
