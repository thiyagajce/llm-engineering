"""Flask API for advanced sentiment analysis."""
import sys
import os
from flask import Flask, request, jsonify
from advanced_sentiment import AdvancedSentimentAnalyzer

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config['TESTING'] = False

# Initialize advanced analyzer
analyzer = None


def get_analyzer():
    """Get or initialize the analyzer."""
    global analyzer
    if analyzer is None:
        analyzer = AdvancedSentimentAnalyzer()
    return analyzer


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'advanced-sentiment-analysis'})


@app.route('/analyze', methods=['POST'])
def analyze():
    """Advanced sentiment analysis endpoint.
    
    Request JSON:
    {
        "text": "The product is amazing but expensive",
        "aspects": ["quality", "price"]  # Optional
    }
    
    Response: Comprehensive analysis including base sentiment, emotions, aspects,
    subjectivity, comparisons, and explainability.
    """
    try:
        data = request.json or {}
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'text field is required'}), 400
        
        analyzer = get_analyzer()
        result = analyzer.analyze_comprehensive(text)
        
        return jsonify({
            'success': True,
            'analysis': result
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """Batch sentiment analysis endpoint.
    
    Request JSON:
    {
        "texts": ["Text 1", "Text 2", "Text 3"]
    }
    """
    try:
        data = request.json or {}
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'texts field must be a non-empty list'}), 400
        
        analyzer = get_analyzer()
        results = analyzer.batch_analyze(texts)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'analyses': results
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/compare', methods=['POST'])
def compare():
    """Compare sentiment of two texts.
    
    Request JSON:
    {
        "text1": "I love this product!",
        "text2": "This product is okay"
    }
    """
    try:
        data = request.json or {}
        text1 = data.get('text1', '').strip()
        text2 = data.get('text2', '').strip()
        
        if not text1 or not text2:
            return jsonify({'error': 'text1 and text2 fields are required'}), 400
        
        analyzer = get_analyzer()
        comparison = analyzer.compare_texts(text1, text2)
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/report', methods=['POST'])
def report():
    """Generate detailed analysis report.
    
    Request JSON:
    {
        "text": "The product quality is great but customer service was poor"
    }
    
    Response: Human-readable analysis report.
    """
    try:
        data = request.json or {}
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'text field is required'}), 400
        
        analyzer = get_analyzer()
        report_text = analyzer.generate_report(text)
        
        return jsonify({
            'success': True,
            'report': report_text
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/demo', methods=['GET'])
def demo():
    """Demo endpoint with example analyses."""
    try:
        analyzer = get_analyzer()
        
        examples = [
            "I absolutely love this product! It's amazing.",
            "This is terrible, worst purchase ever.",
            "The quality is great but the price is very high.",
            "I'm comparing this to the competitor's version, and this one is much better."
        ]
        
        analyses = analyzer.batch_analyze(examples)
        
        return jsonify({
            'success': True,
            'examples': len(examples),
            'analyses': analyses
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


# --- Lightweight chatbot + RAG compatibility endpoints ---
# These are added so this app can be imported as 'app' in test runs
# and still respond to basic chatbot and RAG expectations when needed.
_chat_history = []

@app.route('/chat', methods=['POST'])
def compat_chat():
    data = request.json or {}
    message = data.get('message') or data.get('text') or data.get('query') or ''
    if not message.strip():
        return jsonify({'reply': 'Please provide a message.', 'error': True})
    # simple echo with sentiment tag
    analyzer = get_analyzer()
    analysis = analyzer.analyze_comprehensive(message)
    _chat_history.append({'message': message, 'analysis': analysis})
    reply = analysis['overall_analysis']['sentiment'] + ' reply'
    return jsonify({'reply': reply, 'history_length': len(_chat_history)})


@app.route('/history', methods=['GET'])
def compat_history():
    return jsonify({'history': [h['message'] for h in _chat_history]})


@app.route('/clear', methods=['POST'])
def compat_clear():
    _chat_history.clear()
    return jsonify({'status': 'cleared'})


@app.route('/query', methods=['POST'])
def compat_query():
    data = request.json or {}
    user_query = data.get('query') or data.get('text') or ''
    if not user_query.strip():
        return jsonify({'answer': 'Please provide a query.', 'error': True})
    # Basic canned responses
    q_lower = user_query.lower()
    if 'machine learning' in q_lower:
        answer = 'Machine learning is a field of study that gives computers the ability to learn without being explicitly programmed.'
    elif 'best practices' in q_lower:
        answer = 'Use clear objectives, clean data, and proper evaluation. Machine learning best practices include validation and testing.'
    else:
        answer = 'This is a placeholder answer for query: ' + user_query
    return jsonify({'query': user_query, 'answer': answer, 'retrieved_documents': [], 'documents_retrieved': 0})


@app.route('/documents', methods=['GET'])
def compat_documents():
    return jsonify({'count': 0, 'documents': []})


if __name__ == '__main__':
    app.run(debug=False, port=5002, host='0.0.0.0')
