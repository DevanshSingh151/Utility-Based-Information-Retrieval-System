import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = "ai_utility_search"

# Ensure directories exist
for directory in [DATA_DIR, MODELS_DIR, DOCS_DIR]:
    os.makedirs(directory, exist_ok=True)
