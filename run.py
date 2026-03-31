import os
import sys

os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "120"
os.environ["HF_HUB_DISABLE_XETHUB"] = "1"

# Ensure module visibility
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    from data.generator import generate_sample_data
    from docs.generate_docs import generate_all_docs
    from app.preprocessor import download_nltk_data
    import config
    
    # Setup data and docs on first run
    download_nltk_data()
    print("🚀 Auto-generating Professor Deliverables...")
    generate_all_docs()
    
    print("🚀 Verifying Data and Indexes...")
    generate_sample_data()
    
    print("✅ System Ready. Booting Flask App on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
