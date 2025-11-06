import nltk
from nltk.util import ngrams
from collections import defaultdict
import random

# Download tokenizer data
nltk.download('punkt')
nltk.download('punkt_tab')

# Input text
text = "The quick brown fox jumps over the lazy dog. The fox is very quick and smart."

# --- Step 2: Tokenize the text ---
words = nltk.word_tokenize(text.lower())

# --- Step 3: Create bigrams (pairs of consecutive words) ---
bigrams = list(ngrams(words, 2))
print("Bigrams:", bigrams)

# --- Step 4: Store bigrams in a dictionary ---
bigram_model = defaultdict(list)
for w1, w2 in bigrams:
    bigram_model[w1].append(w2)

# --- Step 5: Generate new text using the bigram model ---
def generate_sentence(start_word, num_words=10):
    word = start_word
    sentence = [word]
    for _ in range(num_words - 1):
        if word not in bigram_model:
            break
        next_word = random.choice(bigram_model[word])
        sentence.append(next_word)
        word = next_word
    return ' '.join(sentence)

# --- Step 6: Test the model ---
print("\nGenerated sentence:")
print(generate_sentence("the"))
