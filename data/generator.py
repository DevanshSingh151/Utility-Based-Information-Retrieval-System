import json
import os
import random
from datetime import datetime, timedelta
from app import config
import math

def generate_sample_data():
    dataset_path = os.path.join(config.DATA_DIR, 'cybersecurity_docs.json')
    if os.path.exists(dataset_path):
        return
        
    print("Generating 1000 sample cybersecurity articles...")
    categories = ["Network Security", "AI Ethics", "Threat Intelligence", "Cryptography", "Cloud Security"]
    sources = ["nytimes", "blog", "academic", "tech_report", "news"]
    
    topics = [
        "AI ethics problems in modern cybersecurity frameworks",
        "New cybersecurity threats 2026 targeting infrastructure",
        "BERT information retrieval techniques for threat hunting",
        "Zero-day exploits in smart home devices",
        "Post-quantum cryptography adoption strategies",
        "Cloud native application protection platforms",
        "Ransomware gangs targeting healthcare in 2026",
        "Federated learning for privacy-preserving AI models",
        "Analysis of advanced persistent threats",
        "Authentication mechanisms using biometrics"
    ]
    
    documents = []
    for i in range(1, 1001):
        base_topic = random.choice(topics)
        doc = {
            "id": f"doc_{i}",
            "title": f"Report {i}: {base_topic.title()} Analysis",
            "content": f"This document discusses {base_topic}. It covers various aspects including methodologies, risk assessments, and emerging trends. Cybersecurity is an ever-evolving field requiring constant vigilance. Furthermore, integration of AI has brought new {random.choice(['challenges', 'opportunities', 'threats'])} to the forefront. " * random.randint(2, 5),
            "category": random.choice(categories),
            "source": random.choice(sources),
            "date": (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d"),
            "readability_score": random.uniform(30.0, 90.0)
        }
        documents.append(doc)
        
    with open(dataset_path, 'w') as f:
        json.dump(documents, f, indent=4)
        
    print("Building Search Indexes (Offline Stage)...")
    from app.retriever.bm25_retriever import BM25Engine
    bm25 = BM25Engine()
    bm25.fit(documents)
    
    from app.retriever.bert_retriever import BERTSearchEngine
    bert = BERTSearchEngine()
    bert.fit(documents)
