# Utility-Based Information Retrieval System

An intelligent, utility-driven hybrid semantic search engine built for complex information retrieval. The system merges traditional BM25 probabilistic retrieval with state-of-the-art BERT embeddings and Cross-Encoder deep neural networks, culminating in a continuous-learning Bayesian Utility Agent.

## Architecture Highlights
- **Hybrid Retrieval:** Reciprocal Rank Fusion (RRF) of Sparse (BM25) and Dense (MiniLM-L6-v2) indexes.
- **Deep Re-ranking:** Cross-Encoder pairwise relevance predictions.
- **Agentic Re-ranking:** A Utility Agent that observes 8 custom features (diversity, recency, trust, cross_score, etc.) to perform the final ranking.
- **Self-Learning Loop:** Bayesian posterior updating using MongoDB to store metrics, implicit feedback, and usage telemetry.
- **Evaluation Engine:** Built-in calculation for MRR, Precision@K, and nDCG metrics.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- MongoDB (optional, falls back to SQLite/JSON if unavailable)

### 2. Local Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env

# First-time Setup: Builds the dataset, indexes, and downloads NLTK properties
python manage.py setup

# Run the API
python run.py
```
*Note: Due to sentence transformers, the initial launch via `manage.py setup` can take a minute to generate offline indexes.*

### 3. Docker Installation
You can easily spin up the application and MongoDB using docker-compose.
```bash
docker-compose up --build
```

## Feedback Learning
User clicks in the UI update the `UtilityAgent`'s internal weight parameters for its 8 dynamic properties. This telemetry is logged dynamically to MongoDB by `FeedbackPersistence`.

## Testing
Run the test suite via Pytest:
```bash
pytest tests/
```
