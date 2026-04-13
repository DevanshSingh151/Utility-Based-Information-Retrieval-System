import numpy as np

def precision_at_k(relevant_ids, retrieved_ids, k):
    if not relevant_ids or not retrieved_ids:
        return 0.0
    top_k = retrieved_ids[:k]
    relevant_retrieved = [doc_id for doc_id in top_k if doc_id in relevant_ids]
    return len(relevant_retrieved) / min(k, len(retrieved_ids))

def mean_reciprocal_rank(relevant_ids, retrieved_ids):
    for rank, doc_id in enumerate(retrieved_ids):
        if doc_id in relevant_ids:
            return 1.0 / (rank + 1)
    return 0.0

def ndcg_at_k(relevance_scores, retrieved_ids, k):
    # relevance_scores dict: {doc_id: score}
    top_k = retrieved_ids[:k]
    dcg = 0.0
    for i, doc_id in enumerate(top_k):
        rel = relevance_scores.get(doc_id, 0)
        dcg += (2**rel - 1) / np.log2(i + 2)
        
    ideal_scores = sorted(list(relevance_scores.values()), reverse=True)[:k]
    idcg = 0.0
    for i, rel in enumerate(ideal_scores):
        idcg += (2**rel - 1) / np.log2(i + 2)
        
    if idcg == 0:
        return 0.0
    return dcg / idcg

def evaluate_system(agent, queries_with_relevance):
    # queries_with_relevance: list of {query: "...", relevant: ["id1", "id2"], relevance_scores: {"id1": 3, "id2": 2}}
    # Mock evaluate structure for tests
    return {
         "precision_at_5": 0.0,
         "mrr": 0.0,
         "ndcg_at_10": 0.0
    }
