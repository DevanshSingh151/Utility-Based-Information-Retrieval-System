import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Define subdirectories
DATA_DIR = os.path.join(BASE_DIR, os.getenv("DATA_DIR", "data"))
MODELS_DIR = os.path.join(BASE_DIR, os.getenv("INDEX_DIR", "models"))
DOCS_DIR = os.path.join(BASE_DIR, os.getenv("DOCS_DIR", "docs"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ai_utility_search")

# Environment vars
FLASK_ENV = os.getenv("FLASK_ENV", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

# Ensure directories exist
for directory in [DATA_DIR, MODELS_DIR, DOCS_DIR]:
    os.makedirs(directory, exist_ok=True)
