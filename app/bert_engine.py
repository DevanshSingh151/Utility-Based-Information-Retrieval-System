import os
import pickle
import math
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
import config

class BERTSearchEngine:
    def __init__(self):
        # We use a lighter model to ensure it loads fast and works without GPU gracefully
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 
        self.corpus_embeddings = None
        self.corpus = []
        
    def fit(self, documents):
        self.corpus = documents
        texts = [doc['content'] for doc in documents]
        print("Generating BERT embeddings... This may take a moment.")
        self.corpus_embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        with open(os.path.join(config.MODELS_DIR, 'bert_index.pkl'), 'wb') as f:
            pickle.dump((self.corpus_embeddings, self.corpus), f)
            
    def load(self):
        path = os.path.join(config.MODELS_DIR, 'bert_index.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.corpus_embeddings, self.corpus = pickle.load(f)
            return True
        return False
        
    def embedding_search(self, query, top_k=100):
        if self.corpus_embeddings is None:
            return []
            
        query_embedding = self.embedding_model.encode([query])
        similarities = cosine_similarity(query_embedding, self.corpus_embeddings)[0]
        
        doc_scores = [{"doc": doc, "score": float(sim)} for doc, sim in zip(self.corpus, similarities)]
        doc_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return doc_scores[:top_k]
        
    def rerank(self, query, top_k_docs):
        if not top_k_docs: return []
        pairs = [[query, doc['doc']['content']] for doc in top_k_docs]
        cross_scores = self.cross_encoder.predict(pairs)
        
        results = []
        for doc_obj, score in zip(top_k_docs, cross_scores):
            # Normalize with sigmoid to keep 0-1
            prob = 1 / (1 + math.exp(-score))
            results.append({
                "doc": doc_obj['doc'],
                "score": float(prob)
            })
            
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

def rrf_fusion(list1, list2, k=60):
    scores = {}
    
    for rank, item in enumerate(list1):
        doc_id = item['doc']['id']
        scores[doc_id] = {"doc": item['doc'], "score": 1.0 / (k + rank), "bert_sim": item['score'], "bm25_sim": 0.0}
        
    for rank, item in enumerate(list2):
        doc_id = item['doc']['id']
        if doc_id not in scores:
            scores[doc_id] = {"doc": item['doc'], "score": 0, "bert_sim": 0.0, "bm25_sim": item['score']}
        scores[doc_id]['score'] += 1.0 / (k + rank)
        if 'bm25_sim' in scores[doc_id] and scores[doc_id]['bm25_sim'] == 0.0:
            scores[doc_id]['bm25_sim'] = item['score']
        
    fused = list(scores.values())
    fused.sort(key=lambda x: x['score'], reverse=True)
    
    # Normalize RRF scores
    if fused:
        max_s = fused[0]['score']
        for item in fused:
            item['score'] /= max_s
            
    return fused
