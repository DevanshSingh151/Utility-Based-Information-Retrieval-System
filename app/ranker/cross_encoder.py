import torch
from sentence_transformers import CrossEncoder

class CrossEncoderRanker:
    def __init__(self):
        self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)

    def rerank(self, query, candidates, top_k=15):
        if not candidates:
            return []
            
        pairs = [[query, res['doc']['content']] for res in candidates]
        
        try:
            scores = self.model.predict(pairs)
            
            # Normalize to [0,1] using sigmoid
            import numpy as np
            scores = 1 / (1 + np.exp(-scores))
            
            for i, res in enumerate(candidates):
                res['cross_score'] = float(scores[i])
                
        except Exception as e:
            # Fall back safely
            print(f"Cross-encoder failure: {e}")
            for res in candidates:
                res['cross_score'] = 0.0
                
        candidates.sort(key=lambda x: x['cross_score'], reverse=True)
        return candidates[:top_k]
