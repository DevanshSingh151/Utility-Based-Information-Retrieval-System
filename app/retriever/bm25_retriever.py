import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi
import string

class BM25Retriever:
    def __init__(self, documents):
        self.documents = documents
        self.stemmer = PorterStemmer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            import logging
            logging.info("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
            
        self.tokenized_corpus = [self._tokenize(doc['content']) for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def _tokenize(self, text):
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = text.split()
        return [self.stemmer.stem(t) for t in tokens if t not in self.stop_words]

    def search(self, query, top_k=50):
        if not self.documents:
            return []
            
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        results = []
        for i, score in enumerate(scores):
            results.append({
                "doc": self.documents[i],
                "bm25_sim": score
            })
            
        # Sort and return top_k
        results.sort(key=lambda x: x['bm25_sim'], reverse=True)
        return results[:top_k]
