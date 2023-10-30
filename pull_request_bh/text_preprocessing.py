import torch
import numpy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

torch.device('cpu')
print(torch.Tensor([1, 2, 3]))

nltk.download('stopwords')
nltk.download('punkt')


def preprocess_text(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Initialize the stemmer
    stemmer = PorterStemmer()

    # Remove stopwords and apply stemming
    filtered_words = [stemmer.stem(word) for word in words if word.lower() not in set(stopwords.words('english'))]

    # Join the filtered words back into a string
    preprocessed_text = ' '.join(filtered_words)

    return preprocessed_text


text = "Text preprocessing in PyTorch involves stemming and removing stop words."
preprocessed_text = preprocess_text(text)
print(preprocessed_text)
