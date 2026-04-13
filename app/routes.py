import os
import time
from flask import Blueprint, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/health', methods=['GET'])
def health():
    from app import search_system
    
    status = "ok" if search_system.bm25_retriever else "initializing"
    
    return jsonify({
        "status": status,
        "documents_loaded": len(search_system.documents),
        "index_ready": search_system.bert_retriever is not None,
        "mongodb": "connected" if (search_system.utility_agent and search_system.utility_agent.persistence.use_mongo) else "failed/JSON_fallback"
    })

@blueprint.route('/search', methods=['POST'])
def search():
    try:
        from app import search_system
        
        # Lazy start if uninitialized (prevents massive stall at startup until actually used)
        if not search_system.hybrid_retriever:
            search_system.initialize_models()
            
        data = request.json
        query = data.get('query')
        user_id = data.get('user_id', 'default')
        
        if not query:
            return jsonify({"error": "Empty query"}), 400
            
        # Temporarily set the agent's user context to grab their specific weights
        local_weights, queries = search_system.utility_agent.persistence.load_weights(search_system.utility_agent.weights.tolist(), user_id)
        search_system.utility_agent.weights = __import__('numpy').array(local_weights)
        search_system.utility_agent.queries_learned = queries
            
        # 1. Hybrid Retrieval (Top 50)
        t0 = time.time()
        hybrid_results = search_system.hybrid_retriever.search(query, top_k=50)
        t_hybrid = time.time() - t0
        
        # 2. Cross Encoder Re-Rerank (Top 15 out of 50)
        t1 = time.time()
        reranked_results = search_system.cross_encoder.rerank(query, hybrid_results, top_k=15)
        t_rerank = time.time() - t1
        
        # 3. Utility Agent Final Scoring (Top 10 out of 15)
        t2 = time.time()
        final_results = search_system.utility_agent.get_ranked_results(query, reranked_results)
        t_utility = time.time() - t2
        
        # Serialize response safely
        response_results = []
        for res in final_results:
            doc = res['doc']
            source_file = doc.get('source_file')
            response_results.append({
                "id": doc['id'],
                "title": doc['title'],
                "content": doc['content'][:300] + "...",
                "domain": doc['domain'],
                "utility": res['utility'],
                "source_file": source_file,
                "has_source": source_file is not None,
                "features": {
                    "cross_encoder": res['features'][0],
                    "bert_similarity": res['features'][1],
                    "bm25_score": res['features'][2],
                    "diversity": res['features'][3],
                    "recency": res['features'][4],
                    "source_trust": res['features'][5],
                    "length_match": res['features'][6],
                    "readability": res['features'][7]
                }
            })
            
        return jsonify({
            "query": query,
            "results": response_results,
            "weights_used": search_system.utility_agent.weights.tolist(),
            "stage_counts": {
                "hybrid": len(hybrid_results),
                "reranked": len(reranked_results),
                "final": len(final_results)
            },
            "timings": {
                "hybrid": round(t_hybrid, 3),
                "rerank": round(t_rerank, 3),
                "utility": round(t_utility, 3)
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@blueprint.route('/feedback', methods=['POST'])
def feedback():
    try:
        from app import search_system
        data = request.json
        user_id = data.get('user_id', 'default')
        
        # Switch agent transient user scope 
        local_weights, queries = search_system.utility_agent.persistence.load_weights(search_system.utility_agent.weights.tolist(), user_id)
        search_system.utility_agent.weights = __import__('numpy').array(local_weights)
        search_system.utility_agent.mu = search_system.utility_agent.weights.copy()
        search_system.utility_agent.queries_learned = queries
        
        updated_weights = search_system.utility_agent.learn_from_feedback(
            query=data['query'],
            doc_id=data['doc_id'],
            features=data['features'],
            clicked=data['clicked']
        )
        
        search_system.utility_agent.persistence.save_weights(updated_weights, search_system.utility_agent.queries_learned, user_id)
        
        return jsonify({
            "updated_weights": updated_weights,
            "queries_learned": search_system.utility_agent.queries_learned,
            "optimal_reached": search_system.utility_agent.optimal_weights_reached
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint.route('/weights/<user_id>', methods=['GET'])
def get_weights(user_id):
    try:
        from app import search_system
        local_weights, queries = search_system.utility_agent.persistence.load_weights(search_system.utility_agent.weights.tolist(), user_id)
        return jsonify({
            "weights": local_weights,
            "feature_names": [
                "Cross Encoder", "BERT Similarity", "BM25 Score", "Diversity",
                "Recency", "Source Trust", "Length Match", "Readability"
            ],
            "queries_learned": queries
        })
    except Exception as e:
         return jsonify({"error": str(e)}), 500

@blueprint.route('/document/<path:filename>', methods=['GET'])
def serve_document(filename):
    """Serve a source document from the documents/ folder so the browser can open it."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docs_dir = os.path.join(base_dir, 'documents')
        return send_from_directory(docs_dir, filename)
    except Exception as e:
        return jsonify({"error": f"File not found: {filename}"}), 404
