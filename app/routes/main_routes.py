from flask import Blueprint, render_template, request, jsonify
from app.retriever.bm25_retriever import BM25Engine
from app.retriever.bert_retriever import BERTSearchEngine, rrf_fusion
from app.ranker.utility_agent import UtilityAgent
from app.utils.snippet import generate_snippet
import time

bp = Blueprint('main', __name__)

bm25 = BM25Engine()
bert = BERTSearchEngine()
agent = UtilityAgent()

# Ensure variables are mapped for global scope
search_engine_ready = False

@bp.before_app_request
def initialize_engines():
    global search_engine_ready
    if not search_engine_ready:
        print("Checking/Loading Offline Indexes...")
        loaded_bm25 = bm25.load()
        loaded_bert = bert.load()
        if loaded_bm25 and loaded_bert:
            print("Offline Indexes loaded successfully in memory.")
            
        search_engine_ready = True

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400
        
    start_time = time.time()
    
    # Stage 1: Hybrid Retrieval
    t0 = time.time()
    bm25_results = bm25.search(query, top_k=100)
    if not bm25_results:
        return jsonify({"error": "No datasets indexed"}), 500
        
    bert_results = bert.embedding_search(query, top_k=100)
    hybrid_top_50 = rrf_fusion(bert_results, bm25_results, k=60)[:50]
    t1 = time.time()
    
    # Stage 2: Cross-Encoder
    cross_results = bert.rerank(query, hybrid_top_50)[:15]
    
    for res in cross_results:
        doc_id = res['doc']['id']
        res['cross_score'] = res['score']
        for h in hybrid_top_50:
            if h['doc']['id'] == doc_id:
                res['bert_sim'] = h['bert_sim']
                res['bm25_sim'] = h['bm25_sim']
                break
    t2 = time.time()
    
    final_results = agent.get_ranked_results(query, cross_results)
    
    # Add snippets
    for res in final_results:
        res['snippet'] = generate_snippet(query, res['doc']['content'])
    t3 = time.time()
    
    return jsonify({
        "results": final_results,
        "timing": {
            "stage_1_ms": round((t1 - t0) * 1000),
            "stage_2_ms": round((t2 - t1) * 1000),
            "stage_3_ms": round((t3 - t2) * 1000),
            "total_ms": round((t3 - start_time) * 1000)
        },
        "agent_status": {
            "queries_learned": agent.queries_learned,
            "optimal": agent.optimal_weights_reached,
            "weights": [round(w, 3) for w in agent.weights.tolist()]
        }
    })

@bp.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    features = data.get('features')
    clicked = data.get('clicked')
    
    query_text = data.get('query', '')
    doc_id = data.get('doc_id', '')
    new_weights = agent.learn_from_feedback(query_text, doc_id, features, clicked)
    
    return jsonify({
        "status": "Learning successful",
        "new_weights": new_weights,
        "queries_learned": agent.queries_learned,
        "optimal": agent.optimal_weights_reached
    })
