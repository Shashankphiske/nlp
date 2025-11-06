# ---- Text Preprocessing using NLTK ----
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

# Download required data (only once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# ---- Sample Text ----
text = "The striped bats are hanging on their feet for best."

# ---- 1. Tokenization ----
tokens = word_tokenize(text)
print("Tokens:", tokens)

# ---- 2. Lowercasing ----
tokens = [word.lower() for word in tokens]

# ---- 3. Remove Punctuation ----
tokens = [word for word in tokens if word not in string.punctuation]

# ---- 4. Stopword Removal ----
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word not in stop_words]
print("After Stopword Removal:", filtered_tokens)

# ---- 5. Stemming ----
stemmer = PorterStemmer()
stemmed = [stemmer.stem(word) for word in filtered_tokens]
print("After Stemming:", stemmed)

# ---- 6. Lemmatization ----
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(word) for word in filtered_tokens]
print("After Lemmatization:", lemmatized)
