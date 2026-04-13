import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from dotenv import load_dotenv

load_dotenv()

class BertRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_dir = os.getenv("INDEX_DIR", "models")
        self.index_path = os.path.join(self.index_dir, "faiss_index.bin")
        self.embed_dim = self.model.get_sentence_embedding_dimension()
        
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
            
        if self.documents:
            self._load_or_build_index()

    def _load_or_build_index(self):
        if os.path.exists(self.index_path):
            print("Loading FAISS index from disk...")
            self.index = faiss.read_index(self.index_path)
            if self.index.ntotal != len(self.documents):
                print("Index size mismatch. Rebuilding FAISS index...")
                self._build_index()
        else:
            print("Building FAISS index for first time...")
            self._build_index()

    def _build_index(self):
        contents = [doc['content'] for doc in self.documents]
        embeddings = self.model.encode(contents, convert_to_numpy=True)
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        
        self.index = faiss.IndexFlatIP(self.embed_dim)
        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_path)
        print(f"FAISS index saved to {self.index_path}")

    def search(self, query, top_k=50):
        if not self.documents:
            return []
            
        query_vector = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_vector)
        
        # Search via FAISS
        distances, indices = self.index.search(query_vector, min(top_k, len(self.documents)))
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append({
                    "doc": self.documents[idx],
                    "bert_sim": float(distances[0][i])
                })
        return results
