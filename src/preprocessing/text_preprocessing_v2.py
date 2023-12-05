import nltk
import pickle
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import sklearn
from sklearn.datasets import fetch_20newsgroups
nltk.download('wordnet')


docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']


class Tokenizer:
    def __init__(self):
        self._tokenizer = nltk.RegexpTokenizer(r'\w+')

    def tokenize(self, document: str) -> list:
        return self._tokenizer.tokenize(document)

class Lemmatizer:
    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()
        self._tokenizer = Tokenizer()

    def _tokenize(self, document: str) -> list:
        return self._tokenizer.tokenize(document)

    def lemmatize_word(self, word: str, pos=None) -> str:
        return self._lemmatizer.lemmatize(word, pos) if pos is not None else self._lemmatizer.lemmatize(word)

    def lemmatize_sentence(self, sentence: str, pos=None) -> str:
        result = []
        for word in self._tokenize(sentence):
            if pos is not None:
                result.append(self.lemmatize_word(word, pos))
            else:
                result.append(self.lemmatize_word(word))
        return ' '.join(result)

    def lemmatize_document(self, document: str) -> str:
        result = []
        for line in document.split('\n'):
            result.append(self.lemmatize_sentence(line))
        return '\n'.join(result)


message = "Have no fear of perfection. You'll never reach it 🔥"
lemmatizer = Lemmatizer()
print(lemmatizer.lemmatize_sentence(message))