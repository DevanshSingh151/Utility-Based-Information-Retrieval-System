# Utility-Based Information Retrieval System
## Hybrid Semantic Search with Bayesian Update Engine

This project creates a robust search engine utilizing documents automatically parsed from local PDFs and PPTs. It routes queries through a 3-stage intelligence pipeline.

### Architectural Pipeline
1. **Hybrid Retrieval**: Extracts top 50 documents using BM25 Sparse Search and Sentence-BERT Dense FAISS Indexing. 
2. **Cross-Encoder Ranker**: Re-runs query against top-50 candidate documents text using `ms-marco-miniLM-L6-V2` bounding the set to top 15 logically grouped results.
3. **Implicit Utility Agent**: Computes an 8-axis feature ranking mathematically scoring results mapped directly across user preference constraints. Learning automatically invokes an explicit Bayesian probabilistic weights update. 

### Quickstart

1. Install Dependencies:
```bash
pip install -r requirements.txt
```

2. Scrape internal PDFs & Build FAISS cache DB models:
```bash
python manage.py index
```

3. Configure user tracking arrays via Mongodb:
```bash
python manage.py setup
```

4. Launch Server:
```bash
python run.py
```
Open `http://localhost:5000` to interact with the Single-Page Search System Frontend GUI.

### Test Console queries
```bash
python manage.py test
```
