# AI Utility Agent Project
## AI Semester Project

**Title:** Adaptive Multi-Objective Utility Agent for Hybrid Semantic Search with Dynamic BERT-Enhanced Retrieval

### Included Features
- Single command setup (pip install + python run.py)
- Zero configuration (all paths auto-detected)
- Flask UI with 8-feature dynamic utility agent ranking
- Module 1/5/7 syllabus coverage built-in
- Auto-generated 1,000 cybersecurity documents dataset
- Auto-generated Professor Report, Slides, and Viva answers
- Built-in `pytest` evaluation suite

### Quickstart
1. Ensure Python 3.10+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the live demo (this automatically generates docs, models, and data):
   ```bash
   python run.py
   ```
4. Access the Demo at `http://localhost:5000`

### Project Description
This application acts as an AI Utility Agent Search Engine. It utilizes BM25 probabilistic retrieval and Sentence-Transformers cross-encoders to find relevant text from 1,000 documents. The true intelligence resides in the Python `UtilityAgent`, which assigns weights to 8 disparate ranking signals, and learns optimal ranking weights in real-time through Bayesian updates based on user positive/negative click signals.
