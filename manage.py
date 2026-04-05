import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def setup_data():
    from data.generator import generate_sample_data
    from docs.generate_docs import generate_all_docs
    from app.utils.preprocessor import download_nltk_data
    
    print("🚀 Downloading NLTK Data...")
    download_nltk_data()
    print("🚀 Auto-generating Professor Deliverables...")
    generate_all_docs()
    
    print("🚀 Verifying Data and Indexes...")
    generate_sample_data()
    print("✅ Setup complete.")

if __name__ == "__main__":
    os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "120"
    os.environ["HF_HUB_DISABLE_XETHUB"] = "1"
    
    parser = argparse.ArgumentParser(description="Manage Utility-Based Information Retrieval System")
    parser.add_argument("command", choices=["setup"], help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_data()
