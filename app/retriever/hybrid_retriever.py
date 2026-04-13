from concurrent.futures import ThreadPoolExecutor

class HybridRetriever:
    def __init__(self, bm25_retriever, bert_retriever):
        self.bm25 = bm25_retriever
        self.bert = bert_retriever

    def search(self, query, top_k=50):
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_bm25 = executor.submit(self.bm25.search, query, top_k)
            future_bert = executor.submit(self.bert.search, query, top_k)
            
            bm25_results = future_bm25.result()
            bert_results = future_bert.result()

        return self._reciprocal_rank_fusion(bm25_results, bert_results, top_k)

    def _reciprocal_rank_fusion(self, bm25_results, bert_results, k=60, top_n=50):
        doc_scores = {}
        doc_data = {}
        bm25_sims = {}
        bert_sims = {}

        # Add BM25 scores
        for rank, res in enumerate(bm25_results):
            doc_id = res['doc']['id']
            doc_data[doc_id] = res['doc']
            score = 1.0 / (k + rank + 1)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + score
            bm25_sims[doc_id] = res['bm25_sim']

        # Add BERT scores
        for rank, res in enumerate(bert_results):
            doc_id = res['doc']['id']
            doc_data[doc_id] = res['doc']
            score = 1.0 / (k + rank + 1)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + score
            bert_sims[doc_id] = res['bert_sim']

        # Format output
        fused_results = []
        for doc_id, rrf_score in doc_scores.items():
            fused_results.append({
                "doc": doc_data[doc_id],
                "bm25_sim": bm25_sims.get(doc_id, 0.0),
                "bert_sim": bert_sims.get(doc_id, 0.0),
                "rrf_score": rrf_score
            })

        # Sort and trim
        fused_results.sort(key=lambda x: x['rrf_score'], reverse=True)
        return fused_results[:top_n]
