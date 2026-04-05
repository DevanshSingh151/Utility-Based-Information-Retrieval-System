import os
import json
import numpy as np
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app import config

class FeedbackPersistence:
    def __init__(self):
        self.use_mongo = False
        self.client = None
        self.db = None
        self.collection = None
        self.local_file = os.path.join(config.DATA_DIR, "agent_weights.json")
        
        try:
            self.client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=2000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[config.MONGO_DB_NAME]
            self.collection = self.db['feedback']
            self.weights_collection = self.db['agent_weights']
            self.use_mongo = True
            print("Connected to MongoDB for feedback loop.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            print("MongoDB unavailable. Falling back to local JSON for feedback persistence.")
            
    def load_weights(self, default_weights):
        if self.use_mongo:
            try:
                record = self.weights_collection.find_one({"_id": "latest"})
                if record and 'weights' in record:
                    return np.array(record['weights']), record.get('queries_learned', 0)
            except Exception as e:
                print(f"Error loading from Mongo: {e}")
                
        # Fallback to local
        if os.path.exists(self.local_file):
            try:
                with open(self.local_file, 'r') as f:
                    data = json.load(f)
                    return np.array(data['weights']), data.get('queries_learned', 0)
            except Exception as e:
                print(f"Error loading from local JSON: {e}")
                
        return np.array(default_weights), 0
        
    def save_weights(self, weights, queries_learned):
        weights_list = [round(w, 4) for w in weights.tolist()]
        data = {
            "weights": weights_list,
            "queries_learned": queries_learned,
            "updated_at": datetime.now().isoformat()
        }
        
        if self.use_mongo:
            try:
                self.weights_collection.update_one(
                    {"_id": "latest"},
                    {"$set": data},
                    upsert=True
                )
            except Exception as e:
                print(f"Error saving to Mongo: {e}")
                
        # Always save local fallback
        try:
            with open(self.local_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving to local JSON: {e}")
            
    def log_interaction(self, query, doc_id, clicked, features):
        log_entry = {
            "query": query,
            "doc_id": doc_id,
            "clicked": clicked,
            "features": [float(f) for f in features],
            "timestamp": datetime.now().isoformat()
        }
        if self.use_mongo:
            try:
                self.collection.insert_one(log_entry)
            except Exception as e:
                pass
