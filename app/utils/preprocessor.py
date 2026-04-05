import nltk
import re

def download_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK requirements...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)

class Preprocessor:
    def __init__(self):
        download_nltk_data()
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        from nltk.tokenize import word_tokenize
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return " ".join(tokens)
