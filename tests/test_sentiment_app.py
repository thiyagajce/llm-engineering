"""Integration tests for the advanced sentiment analysis API."""
import pytest
import sys
import os
import json

# Add paths for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sentiment_path = os.path.join(project_root, 'ai-projects', 'projects', 'sentiment-analysis')
sys.path.insert(0, sentiment_path)

# Change to sentiment analysis directory for imports
original_dir = os.getcwd()
os.chdir(sentiment_path)

try:
    from app import app as sentiment_app
finally:
    os.chdir(original_dir)


@pytest.fixture
def sentiment_client():
    """Create Flask test client for sentiment analysis app."""
    sentiment_app.config['TESTING'] = True
    with sentiment_app.test_client() as client:
        yield client


class TestAdvancedSentimentAPI:
    """Tests for advanced sentiment analysis API endpoints."""
    
    def test_health_endpoint(self, sentiment_client):
        """Test health check endpoint."""
        response = sentiment_client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'sentiment' in data['service']
    
    def test_analyze_positive_text(self, sentiment_client):
        """Test analyzing positive text."""
        payload = {'text': 'I absolutely love this product! It\'s amazing!'}
        response = sentiment_client.post('/analyze', 
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        analysis = data['analysis']
        
        # Check overall sentiment
        assert 'overall_analysis' in analysis
        assert analysis['overall_analysis']['sentiment'] == 'positive'
        
        # Check emotion
        assert 'emotion_analysis' in analysis
        assert 'primary_emotion' in analysis['emotion_analysis']
        
        # Check subjectivity
        assert 'subjectivity' in analysis
        assert 'label' in analysis['subjectivity']
    
    def test_analyze_negative_text(self, sentiment_client):
        """Test analyzing negative text."""
        payload = {'text': 'This is terrible and awful!'}
        response = sentiment_client.post('/analyze', 
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        analysis = data['analysis']
        assert analysis['overall_analysis']['sentiment'] == 'negative'
    
    def test_analyze_aspect_sentiment(self, sentiment_client):
        """Test analyzing aspect sentiment."""
        payload = {'text': 'Great quality but very expensive product'}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        analysis = data['analysis']
        
        # Check aspects
        assert 'aspect_sentiment' in analysis
        aspects = analysis['aspect_sentiment']
        # Should detect quality and price aspects
        assert isinstance(aspects, dict)
    
    def test_analyze_empty_text(self, sentiment_client):
        """Test error handling for empty text."""
        payload = {'text': ''}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_analyze_missing_text_field(self, sentiment_client):
        """Test error handling for missing text field."""
        payload = {}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 400
    
    def test_analyze_includes_explainability(self, sentiment_client):
        """Test that analysis includes explainability information."""
        payload = {'text': 'I love this wonderful product'}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        analysis = data['analysis']
        
        assert 'explainability' in analysis
        explainability = analysis['explainability']
        assert 'top_features' in explainability
        assert 'explanation' in explainability
        assert 'positive_words' in explainability
        assert 'negative_words' in explainability
    
    def test_batch_analyze(self, sentiment_client):
        """Test batch analysis endpoint."""
        payload = {
            'texts': [
                'I love this!',
                'This is terrible',
                'It\'s okay'
            ]
        }
        response = sentiment_client.post('/batch-analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert data['count'] == 3
        assert 'analyses' in data
        assert len(data['analyses']) == 3
    
    def test_batch_analyze_empty_list(self, sentiment_client):
        """Test batch analysis with empty list."""
        payload = {'texts': []}
        response = sentiment_client.post('/batch-analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 400
    
    def test_batch_analyze_invalid_format(self, sentiment_client):
        """Test batch analysis with invalid format."""
        payload = {'texts': 'not_a_list'}
        response = sentiment_client.post('/batch-analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 400
    
    def test_compare_texts(self, sentiment_client):
        """Test text comparison endpoint."""
        payload = {
            'text1': 'I love this product!',
            'text2': 'I hate this product'
        }
        response = sentiment_client.post('/compare',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        comparison = data['comparison']
        
        assert 'text1_sentiment' in comparison
        assert 'text2_sentiment' in comparison
        assert 'more_positive' in comparison
        assert comparison['text1_sentiment'] == 'positive'
        assert comparison['text2_sentiment'] == 'negative'
    
    def test_compare_similar_texts(self, sentiment_client):
        """Test comparing similar sentiment texts."""
        payload = {
            'text1': 'This is good',
            'text2': 'This is nice'
        }
        response = sentiment_client.post('/compare',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        comparison = data['comparison']
        # Should be close in sentiment
        assert abs(comparison['score_difference']) <= 1.0
    
    def test_compare_missing_text(self, sentiment_client):
        """Test comparison with missing text field."""
        payload = {'text1': 'Some text'}
        response = sentiment_client.post('/compare',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 400
    
    def test_report_endpoint(self, sentiment_client):
        """Test report generation endpoint."""
        payload = {
            'text': 'The product quality is excellent but customer service was poor'
        }
        response = sentiment_client.post('/report',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'report' in data
        
        report = data['report']
        assert isinstance(report, str)
        assert len(report) > 0
        # Check that report contains expected sections
        assert '=' in report  # Report formatting
    
    def test_report_missing_text(self, sentiment_client):
        """Test report generation with missing text."""
        payload = {}
        response = sentiment_client.post('/report',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 400
    
    def test_demo_endpoint(self, sentiment_client):
        """Test demo endpoint."""
        response = sentiment_client.get('/demo')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'analyses' in data
        assert 'examples' in data
        assert data['examples'] > 0
        assert len(data['analyses']) == data['examples']
    
    def test_analysis_response_structure(self, sentiment_client):
        """Test that analysis response has expected structure."""
        payload = {'text': 'This is a test'}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        data = json.loads(response.data)
        analysis = data['analysis']
        
        # Verify complete structure
        assert 'text' in analysis
        assert 'overall_analysis' in analysis
        assert 'emotion_analysis' in analysis
        assert 'aspect_sentiment' in analysis
        assert 'subjectivity' in analysis
        assert 'comparative_analysis' in analysis
        assert 'explainability' in analysis
        
        # Verify nested structures
        overall = analysis['overall_analysis']
        assert 'sentiment' in overall
        assert 'confidence' in overall
        assert 'score' in overall
        
        emotion = analysis['emotion_analysis']
        assert 'primary_emotion' in emotion
        assert 'confidence' in emotion
        assert 'emotion_scores' in emotion
    
    def test_multiple_sequential_requests(self, sentiment_client):
        """Test multiple sequential API requests."""
        texts = [
            'Great product!',
            'Not satisfied',
            'Excellent quality'
        ]
        
        for text in texts:
            payload = {'text': text}
            response = sentiment_client.post('/analyze',
                                           data=json.dumps(payload),
                                           content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success']
    
    def test_special_characters_in_text(self, sentiment_client):
        """Test handling special characters in text."""
        payload = {
            'text': 'Great!!! Love it!!! 😍 #awesome @brand'
        }
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]


class TestAdvancedSentimentComparative:
    """Comparative analysis tests for different text types."""
    
    def test_review_analysis(self, sentiment_client):
        """Test analyzing a product review."""
        review = "Excellent product with great quality. Highly recommended!"
        payload = {'text': review}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['analysis']['overall_analysis']['sentiment'] == 'positive'
    
    def test_complaint_analysis(self, sentiment_client):
        """Test analyzing a complaint."""
        complaint = "Very disappointed. Poor quality and bad customer service."
        payload = {'text': complaint}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['analysis']['overall_analysis']['sentiment'] == 'negative'
    
    def test_factual_text_analysis(self, sentiment_client):
        """Test analyzing factual text."""
        factual = "The product has 100GB storage, weighs 200 grams, and costs $50."
        payload = {'text': factual}
        response = sentiment_client.post('/analyze',
                                         data=json.dumps(payload),
                                         content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Factual text should be more objective
        subjectivity = data['analysis']['subjectivity']
        assert 'label' in subjectivity


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
