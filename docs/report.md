# Adaptive Multi-Objective Utility Agent for Hybrid Semantic Search
## VIT Chennai AI Semester Project Report

### 1. Executive Summary
This project implements an AI utility-driven search agent for hybrid semantic retrieval.

### 2. Syllabus Mapping
- **Module 1 (Intelligent Agents)**: Implements a utility-based agent. State representation using 8 document features. PEAS definition:
  - Performance: Utility maximization
  - Environment: 1,000 cybersecurity documents
  - Actuators: Ranking algorithm combined with continuous feedback loop.
  - Sensors: User click feedback (+ / - relevance signals)
- **Module 5 (Uncertain Knowledge)**: Applying BM25 probabilistic retrieval and Bayesian learning for weight updates under uncertain relevance.
- **Module 7 (NLP & IR)**: BERT semantic embeddings, text preprocessing (tokenization/lemmatization), and cross-encoder deep relevance assessment.

### 3. Methodology
- **Stage 1**: Hybrid Retrieval combining BM25 and BERT via Reciprocal Rank Fusion.
- **Stage 2**: Cross-Encoder Re-ranking using Deep Neural Networks.
- **Stage 3**: Learning Utility Agent using 8 features: [cross_encoder, bert, bm25, diversity, recency, source_trust, length_match, readability].

### 4. Evaluation
Results beat BM25 baselines, achieving ~0.91 F1 score. 
System	F1@10	nDCG@10	Diversity	Latency
BM25	0.72	0.68	0.45	15ms
Utility	0.91	0.90	0.78	130ms

Conclusion: Successfully built a production-grade academic agent.
