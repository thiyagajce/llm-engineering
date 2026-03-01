from flask import Flask, request, jsonify
from pathlib import Path
from rag_system import RAGSystem

app = Flask(__name__)
rag = RAGSystem()

# Load sample documents on startup
@app.before_first_request
def load_documents():
    """Load documents on first request."""
    docs_dir = Path(__file__).parent.parent.parent / 'datasets' / 'docs'
    if docs_dir.exists():
        try:
            rag.load_documents(docs_dir)
        except Exception as e:
            print(f"Warning: Could not load documents: {e}")

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/query', methods=['POST'])
def query():
    data = request.json or {}
    user_query = data.get('query', '')
    
    if not user_query.strip():
        return jsonify({'answer': 'Please provide a query.', 'error': True})
    
    # Generate answer using RAG
    result = rag.generate_answer(user_query)
    
    return jsonify({
        'query': result['query'],
        'answer': result['answer'],
        'documents_retrieved': len(result['retrieved_documents']),
        'retrieved_docs': [
            {'title': doc['title'], 'score': doc['score']}
            for doc in result['retrieved_documents']
        ]
    })

@app.route('/documents', methods=['GET'])
def documents():
    """Get all loaded documents."""
    docs = rag.store.get_all_documents()
    return jsonify({
        'count': len(docs),
        'documents': [
            {'title': doc['title'], 'preview': doc['content'][:100]}
            for doc in docs
        ]
    })

if __name__ == '__main__':
    app.run(port=5003, debug=True)
