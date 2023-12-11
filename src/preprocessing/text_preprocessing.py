import nltk
import pickle
from collections import Counter
import pickle
import numpy as np
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import sklearn
from sklearn.datasets import fetch_20newsgroups

nltk.download('wordnet')


# docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']
class Tokenizer:
    def __init__(self):
        self._tokenizer = nltk.RegexpTokenizer(r'\w+')

    def tokenize(self, document: str) -> list:
        return self._tokenizer.tokenize(document)


class Lemmatizer:
    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()
        self._tokenizer = Tokenizer()
        self._stopwords = list(set(stopwords.words("english")))
        self._custom_stop_words = ['the', 'and', 'is', 'in', 'it', 'of', 'for', 'to', 'with', 'on']
        self._stopwords.extend(
            ['two', 'one', 'way', 'pt', 'from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_',
             'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see',
             'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line',
             'even', 'also', 'may', 'take', 'come'])

    def _tokenize(self, document: str) -> list:
        return self._tokenizer.tokenize(document)

    def _remove_special_characters_and_numbers(self, word) -> str:
        # Remove special characters and numbers using regular expressions
        cleaned_text = re.sub(r'[^A-Za-z\s]', '', word)  # Remove special characters
        cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)  # Remove standalone numbers
        return cleaned_text

    def lemmatize_word(self, word: str, pos=None) -> str:
        return self._lemmatizer.lemmatize(word, pos) if pos is not None else self._lemmatizer.lemmatize(word)

    def lemmatize_sentence(self, sentence: str, pos=None) -> str:
        result = []
        sentence = sentence.lower()
        for word in self._tokenize(sentence):
            word = self._remove_special_characters_and_numbers(word)
            if word.lower() in self._stopwords or word.lower() in self._custom_stop_words or len(word) < 3:
                continue
            if pos is not None:
                result.append(self.lemmatize_word(word, pos))
            else:
                result.append(self.lemmatize_word(word))
        return result

    def lemmatize_document(self, document: list) -> str:
        result = []
        for line in document:
            result.append(self.lemmatize_sentence(line))
        return result
