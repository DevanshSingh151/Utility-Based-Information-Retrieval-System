import os
import json
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class FeedbackPersistence:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("MONGO_DB_NAME", "ai_utility_search")
        self.use_mongo = False
        
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
            self.client.server_info()
            self.db = self.client[self.db_name]
            self.weights_col = self.db['user_weights']
            self.logs_col = self.db['interaction_logs']
            self.use_mongo = True
            logging.info("Connected to MongoDB successfully.")
        except Exception as e:
            logging.warning(f"MongoDB connection failed: {e}. Falling back to local JSON persistence.")
            self.fallback_file = os.path.join(os.getenv("DATA_DIR", "data"), "weights.json")

    def save_weights(self, weights: list, queries_learned: int, user_id="default"):
        try:
            if self.use_mongo:
                self.weights_col.update_one(
                    {"user_id": user_id},
                    {"$set": {"weights": weights, "queries_learned": queries_learned}},
                    upsert=True
                )
            else:
                data = self._load_local()
                data[user_id] = {"weights": weights, "queries_learned": queries_learned}
                self._save_local(data)
        except Exception as e:
            logging.error(f"Error saving weights: {e}")

    def load_weights(self, default_weights: list, user_id="default"):
        try:
            if self.use_mongo:
                record = self.weights_col.find_one({"user_id": user_id})
                if record:
                    return record.get("weights", default_weights), record.get("queries_learned", 0)
            else:
                data = self._load_local()
                if user_id in data:
                    return data[user_id].get("weights", default_weights), data[user_id].get("queries_learned", 0)
        except Exception as e:
            logging.error(f"Error loading weights: {e}")
        return default_weights, 0

    def log_interaction(self, query, doc_id, clicked, features, user_id="default"):
        try:
            log_entry = {
                "user_id": user_id,
                "query": query,
                "doc_id": doc_id,
                "clicked": clicked,
                "features": features
            }
            if self.use_mongo:
                self.logs_col.insert_one(log_entry)
            else:
                pass # Simple fallback doesn't log interaction volume for now
        except Exception as e:
            logging.error(f"Error logging interaction: {e}")

    def _load_local(self):
        if not os.path.exists(self.fallback_file):
            return {}
        with open(self.fallback_file, 'r') as f:
            return json.load(f)

    def _save_local(self, data):
        with open(self.fallback_file, 'w') as f:
            json.dump(data, f)
