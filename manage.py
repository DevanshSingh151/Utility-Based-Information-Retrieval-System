import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def setup_db():
    print("Setting up MongoDB indexes...")
    from app.feedback.persistence import FeedbackPersistence
    fp = FeedbackPersistence()
    if fp.use_mongo:
        fp.weights_col.create_index("user_id", unique=True)
        fp.logs_col.create_index("user_id")
        print("MongoDB collections and indexes created.")
    else:
        print("Using local JSON fallback, nothing to index in MongoDB.")

def build_index():
    from data.generator import generate_sample_data
    print("Generating/Parsing chunks from local documents...")
    generate_sample_data()
    
    print("Pre-warming Search Models (BM25, FAISS build)...")
    from app import search_system
    search_system.initialize_models()
    print("Indexing complete.")

def test():
    print("Testing 5 sample queries...")
    from app import search_system
    search_system.initialize_models()
    
    test_queries = [
        "what is round robin scheduling",
        "difference between relational algebra and sql",
        "instruction pipeline hazards",
        "eigenvalues in computer vision",
        "informed search algorithms"
    ]
    
    for q in test_queries:
        print(f"\nQuery: {q}")
        hybrid_res = search_system.hybrid_retriever.search(q, top_k=50)
        reranked = search_system.cross_encoder.rerank(q, hybrid_res, top_k=15)
        finals = search_system.utility_agent.get_ranked_results(q, reranked)
        print("  Top result:")
        if finals:
            doc = finals[0]['doc']
            print(f"    [{doc['domain']}] {doc['title']}")
            print(f"    Utility: {finals[0]['utility']} | Features: {finals[0]['features']}")
        else:
            print("    No results found.")

def evaluate():
    print("Evaluating system not fully implemented without relevance judgements.")
    from app.evaluation.metrics import evaluate_system
    res = evaluate_system(None, [])
    print(f"Evaluation metrics: {res}")

def reset():
    print("Clearing all learned weights...")
    import json
    weights_path = os.path.join("data", "weights.json")
    if os.path.exists(weights_path):
        os.remove(weights_path)
    print("Cleared local weights JSON. MongoDB requires manual wipe.")

if __name__ == "__main__":
    os.environ["HF_HUB_DISABLE_XETHUB"] = "1"
    parser = argparse.ArgumentParser(description="Manage Search System")
    parser.add_argument("command", choices=["setup", "index", "test", "evaluate", "reset"], help="Command to run")
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_db()
    elif args.command == "index":
        build_index()
    elif args.command == "test":
        test()
    elif args.command == "evaluate":
        evaluate()
    elif args.command == "reset":
        reset()
