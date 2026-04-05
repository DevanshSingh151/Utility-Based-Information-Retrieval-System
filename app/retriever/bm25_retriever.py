import os
import pickle
import math
from rank_bm25 import BM25Okapi
from app import config
from app.utils.preprocessor import Preprocessor

class BM25Engine:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.bm25 = None
        self.corpus = []
        
    def fit(self, documents):
        self.corpus = documents
        tokenized_corpus = [self.preprocessor.clean_text(doc['content']).split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        with open(os.path.join(config.MODELS_DIR, 'bm25_index.pkl'), 'wb') as f:
            pickle.dump((self.bm25, self.corpus), f)
            
    def load(self):
        path = os.path.join(config.MODELS_DIR, 'bm25_index.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.bm25, self.corpus = pickle.load(f)
            return True
        return False
        
    def search(self, query, top_k=100):
        if not self.bm25:
            return []
        tokenized_query = self.preprocessor.clean_text(query).split()
        scores = self.bm25.get_scores(tokenized_query)
        doc_scores = [{"doc": doc, "score": float(score)} for doc, score in zip(self.corpus, scores)]
        doc_scores.sort(key=lambda x: x['score'], reverse=True)
        
        if doc_scores:
            max_score = doc_scores[0]['score'] if doc_scores[0]['score'] > 0 else 1
            for res in doc_scores:
                res['score'] = res['score'] / max_score
                
        return doc_scores[:top_k]
