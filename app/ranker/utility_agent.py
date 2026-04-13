import numpy as np
from datetime import datetime

from app.feedback.persistence import FeedbackPersistence

class UtilityAgent:
    def __init__(self):
        # 8 Dynamic Features
        # [cross_encoder_score, bert_similarity, bm25_score, diversity_mmr, recency_factor, source_trust, length_match, readability_match]
        default_weights = [0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.07, 0.03]
        self.persistence = FeedbackPersistence()
        
        loaded_weights, queries = self.persistence.load_weights(default_weights)
        self.weights = np.array(loaded_weights)
        self.mu = self.weights.copy()
        self.sigma2 = np.ones(8) * 0.1 # Prior variance
        
        self.learning_rate = 0.05
        self.queries_learned = queries
        self.optimal_weights_reached = queries >= 10
        
    def bayesian_uniform_prior(self):
        return np.ones(8) / 8.0
        
    def _calculate_recency(self, date_str):
        try:
            doc_date = datetime.strptime(date_str, "%Y-%m-%d")
            days_old = (datetime.now() - doc_date).days
            return max(0, 1.0 / (days_old + 1))
        except:
            return 0.0
            
    def _calculate_source_trust(self, source):
        trust_map = {
            "nytimes": 0.95,
            "academic": 0.90,
            "tech_report": 0.85,
            "news": 0.70,
            "blog": 0.40
        }
        return trust_map.get(source, 0.5)
        
    def _calculate_length_match(self, query_len, doc_len):
        diff = abs(query_len - doc_len)
        return max(0, 1.0 - (diff / 5000.0))
        
    def _calculate_readability_match(self, doc_score):
        diff = abs(doc_score - 60.0)
        return max(0, 1.0 - (diff / 100.0))

    def extract_features(self, query, doc_obj, bert_sim, bm25_sim, cross_score, diversity_mmr=1.0):
        query_len = len(query.split())
        doc_len = len(doc_obj['content'].split())
        
        features = np.array([
            cross_score,
            bert_sim,
            bm25_sim,
            diversity_mmr,
            self._calculate_recency(doc_obj['date']),
            self._calculate_source_trust(doc_obj['source']),
            self._calculate_length_match(query_len, doc_len),
            self._calculate_readability_match(doc_obj['readability_score'])
        ])
        return np.clip(features, 0.0, 1.0)
        
    def compute_utility(self, features):
        return np.dot(self.weights, features)
        
    def get_ranked_results(self, query, hybrid_results):
        ranked = []
        for res in hybrid_results:
            doc = res['doc']
            feats = self.extract_features(
                query, 
                doc, 
                res.get('bert_sim', 0), 
                res.get('bm25_sim', 0), 
                res.get('cross_score', res.get('score', 0))
            )
            utility = self.compute_utility(feats)
            ranked.append({
                "doc": doc,
                "features": [round(f, 3) for f in feats.tolist()],
                "utility": round(float(utility), 3)
            })
            
        ranked.sort(key=lambda x: x['utility'], reverse=True)
        return ranked[:10]
        
    def learn_from_feedback(self, query, doc_id, features, clicked):
        # Explicit Bayesian Update (Gaussian Conjugate Prior Assuming Diagonal Covariance)
        x = np.array(features)
        y = 1.0 if clicked else -1.0
        noise_var = 0.5  # Assumed noise variance in user observation
        
        for i in range(len(self.mu)):
            precision_prior = 1.0 / self.sigma2[i]
            precision_data = (x[i]**2) / noise_var
            
            precision_post = precision_prior + precision_data
            self.sigma2[i] = 1.0 / precision_post
            
            self.mu[i] = self.sigma2[i] * (precision_prior * self.mu[i] + (x[i] * y) / noise_var)
            
        self.mu = np.clip(self.mu, 0.01, 1.0)
        self.mu = self.mu / np.sum(self.mu) # Normalize to maintain probabilistic distribution constraint
        
        self.weights = self.mu.copy()
        
        self.persistence.log_interaction(query, doc_id, clicked, features)
        
        if clicked:
            self.queries_learned += 1
            if self.queries_learned >= 10:
                self.optimal_weights_reached = True
                
        self.persistence.save_weights(self.weights.tolist(), self.queries_learned)
                
        return [round(w, 3) for w in self.weights.tolist()]
