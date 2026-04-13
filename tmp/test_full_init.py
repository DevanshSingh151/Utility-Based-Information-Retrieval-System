import os
import sys
import logging

# Add the current directory to sys.path to find 'app'
sys.path.append(os.getcwd())

logging.basicConfig(level=logging.INFO)

def test_init():
    try:
        from app import search_system
        print("Starting initialization...")
        search_system.initialize_models()
        print("Initialization complete!")
        
        print("Testing search...")
        from flask import Flask
        # Minimal mock request context if needed, but search_system methods don't seem to need it
        results = search_system.hybrid_retriever.search("CPU", top_k=5)
        print(f"Hybrid search found {len(results)} results.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_init()
