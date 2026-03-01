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
    return jsonify({'status': 'healthy', 'service': 'advanced-sentiment-analysis'})


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


if __name__ == '__main__':
    app.run(debug=False, port=5002, host='0.0.0.0')
