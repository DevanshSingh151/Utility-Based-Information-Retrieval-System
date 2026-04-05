import math
import numpy as np

def calculate_precision_at_k(relevant_docs, retrieved_docs, k):
    """
    Computes Precision@K.
    """
    if k == 0:
        return 0.0
    retrieved = [doc['doc']['id'] for doc in retrieved_docs[:k]]
    relevant = set(relevant_docs)
    
    hits = sum(1 for doc_id in retrieved if doc_id in relevant)
    return hits / float(k)

def calculate_mrr(relevant_docs, retrieved_docs):
    """
    Computes Mean Reciprocal Rank.
    """
    relevant = set(relevant_docs)
    for rank, doc in enumerate(retrieved_docs, start=1):
        if doc['doc']['id'] in relevant:
            return 1.0 / rank
    return 0.0

def calculate_ndcg_at_k(relevant_docs, retrieved_docs, k):
    """
    Computes normalized Discounted Cumulative Gain at K.
    Assume binary relevance (1 if in relevant_docs else 0).
    """
    dcg = 0.0
    idcg = 0.0
    relevant = set(relevant_docs)
    
    # Calculate DCG
    for i, doc in enumerate(retrieved_docs[:k]):
        rel = 1 if doc['doc']['id'] in relevant else 0
        dcg += (2**rel - 1) / math.log2(i + 2)
        
    # Calculate IDCG (Ideal DCG)
    ideal_rels = sorted([1 if i < len(relevant) else 0 for i in range(k)], reverse=True)
    for i, rel in enumerate(ideal_rels):
        idcg += (2**rel - 1) / math.log2(i + 2)
        
    if idcg == 0:
        return 0.0
    return dcg / idcg

def evaluate_system(test_cases, retriever_func, k=10):
    """
    Runs evaluation over a set of test cases.
    test_cases: List of dicts, e.g., [{"query": "AI problems", "relevant_docs": ["doc_1", "doc_5"]}]
    """
    metrics = {
        f"precision@{k}": [],
        "mrr": [],
        f"ndcg@{k}": []
    }
    
    for case in test_cases:
        query = case['query']
        relevant_docs = case['relevant_docs']
        
        results = retriever_func(query)
        
        p_k = calculate_precision_at_k(relevant_docs, results, k)
        mrr = calculate_mrr(relevant_docs, results)
        ndcg_k = calculate_ndcg_at_k(relevant_docs, results, k)
        
        metrics[f"precision@{k}"].append(p_k)
        metrics["mrr"].append(mrr)
        metrics[f"ndcg@{k}"].append(ndcg_k)
        
    return {
        f"mean_precision@{k}": np.mean(metrics[f"precision@{k}"]),
        "mean_mrr": np.mean(metrics["mrr"]),
        f"mean_ndcg@{k}": np.mean(metrics[f"ndcg@{k}"])
    }
