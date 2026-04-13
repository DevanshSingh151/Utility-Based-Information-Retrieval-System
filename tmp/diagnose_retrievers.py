import os
import json
import logging
from app.retriever.bm25_retriever import BM25Retriever
from app.retriever.bert_retriever import BertRetriever

logging.basicConfig(level=logging.INFO)

def diagnose():
    data_path = os.path.join("data", "documents.json")
    print(f"Loading documents from {data_path}...")
    with open(data_path, "r", encoding="utf-8") as f:
        documents = json.load(f)
    print(f"Loaded {len(documents)} documents.")

    print("Initializing BM25...")
    bm25 = BM25Retriever(documents)
    print("BM25 initialized.")

    print("Initializing BERT (this might take time)...")
    bert = BertRetriever(documents)
    print("BERT initialized.")
    
    print("Testing BERT search...")
    res = bert.search("CPU", top_k=5)
    print(f"Found {len(res)} results.")
    for r in res:
        print(f" - {r['doc']['id']}: {r['bert_sim']}")

if __name__ == "__main__":
    diagnose()
