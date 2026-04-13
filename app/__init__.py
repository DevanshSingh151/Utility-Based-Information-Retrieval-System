import os
import json
from flask import Flask
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

class SearchApp:
    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        
        # We will load these lazily or during first request to keep __init__ clean
        self.documents = []
        self.bm25_retriever = None
        self.bert_retriever = None
        self.hybrid_retriever = None
        self.cross_encoder = None
        self.utility_agent = None

    def initialize_models(self):
        # Load from documents.json
        data_path = os.path.join(os.getenv("DATA_DIR", "data"), "documents.json")
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
            logging.info(f"Loaded {len(self.documents)} documents.")
        except Exception as e:
            logging.error(f"Error loading documents.json: {e}")
            self.documents = []

        from app.retriever.bm25_retriever import BM25Retriever
        from app.retriever.bert_retriever import BertRetriever
        from app.retriever.hybrid_retriever import HybridRetriever
        from app.ranker.cross_encoder import CrossEncoderRanker
        from app.ranker.utility_agent import UtilityAgent

        logging.info("Initializing BM25 + BERT pipeline...")
        self.bm25_retriever = BM25Retriever(self.documents)
        self.bert_retriever = BertRetriever(self.documents)
        self.hybrid_retriever = HybridRetriever(self.bm25_retriever, self.bert_retriever)
        
        logging.info("Initializing Cross-Encoder...")
        self.cross_encoder = CrossEncoderRanker()
        
        logging.info("Initializing Utility Agent...")
        self.utility_agent = UtilityAgent()
        
        logging.info("All components initialized successfully!")

    def register_routes(self):
        from app.routes import blueprint
        self.app.register_blueprint(blueprint)

search_system = SearchApp()

def create_app():
    search_system.register_routes()
    return search_system.app
