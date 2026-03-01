"""Integration tests for Flask applications."""
import sys
import json
from pathlib import Path
import pytest


chatbot_dir = Path(__file__).parent.parent / 'ai-projects' / 'projects' / 'chatbot'
sys.path.insert(0, str(chatbot_dir))


@pytest.fixture
def chatbot_client():
    """Create chatbot test client."""
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(str(chatbot_dir))
        import sys
        if 'app' in sys.modules:
            del sys.modules['app']
        from app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    finally:
        os.chdir(old_cwd)


class TestChatbotIntegration:
    """Integration tests for chatbot Flask app."""
    
    def test_full_conversation_flow(self, chatbot_client):
        """Test complete conversation flow."""
        # Start with greeting
        resp1 = chatbot_client.post('/chat', json={'message': 'Hello'})
        assert resp1.status_code == 200
        data1 = json.loads(resp1.data)
        assert 'reply' in data1
        
        # Ask a question
        resp2 = chatbot_client.post('/chat', json={'message': 'What can you do?'})
        assert resp2.status_code == 200
        data2 = json.loads(resp2.data)
        assert 'reply' in data2
        assert data2.get('history_length') == 2
        
        # Say goodbye
        resp3 = chatbot_client.post('/chat', json={'message': 'goodbye'})
        assert resp3.status_code == 200
        data3 = json.loads(resp3.data)
        assert data3.get('history_length') == 3
    
    def test_history_endpoint(self, chatbot_client):
        """Test history retrieval."""
        # Send some messages
        chatbot_client.post('/chat', json={'message': 'Hi'})
        chatbot_client.post('/chat', json={'message': 'Test'})
        
        # Get history
        resp = chatbot_client.get('/history')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'history' in data
        assert len(data['history']) == 2
    
    def test_clear_history_endpoint(self, chatbot_client):
        """Test history clearing."""
        # Add messages
        chatbot_client.post('/chat', json={'message': 'Test'})
        
        # Clear
        resp = chatbot_client.post('/clear')
        assert resp.status_code == 200
        
        # Verify cleared
        history_resp = chatbot_client.get('/history')
        history_data = json.loads(history_resp.data)
        assert len(history_data['history']) == 0
    
    def test_error_handling_empty_message(self, chatbot_client):
        """Test error handling for empty messages."""
        resp = chatbot_client.post('/chat', json={'message': ''})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'error' in data or 'reply' in data


rag_dir = Path(__file__).parent.parent / 'ai-projects' / 'projects' / 'rag-system'
sys.path.insert(0, str(rag_dir))


@pytest.fixture
def rag_client():
    """Create RAG system test client."""
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(str(rag_dir))
        import sys
        if 'app' in sys.modules:
            del sys.modules['app']
        from app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    finally:
        os.chdir(old_cwd)


class TestRAGIntegration:
    """Integration tests for RAG system Flask app."""
    
    def test_documents_endpoint(self, rag_client):
        """Test document retrieval endpoint."""
        resp = rag_client.get('/documents')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'count' in data
        assert 'documents' in data
    
    def test_query_endpoint(self, rag_client):
        """Test query endpoint."""
        resp = rag_client.post('/query', json={
            'query': 'test document'
        })
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'answer' in data
        assert 'query' in data
        assert 'documents_retrieved' in data
    
    def test_multiple_queries(self, rag_client):
        """Test multiple sequential queries."""
        queries = ['test', 'python', 'document']
        for q in queries:
            resp = rag_client.post('/query', json={'query': q})
            assert resp.status_code == 200
            assert 'answer' in json.loads(resp.data)
    
    def test_empty_query_handling(self, rag_client):
        """Test handling of empty query."""
        resp = rag_client.post('/query', json={'query': ''})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'error' in data or 'answer' in data


class TestCrossSystemIntegration:
    """Integration tests across multiple systems."""
    
    def test_health_checks(self, chatbot_client, rag_client):
        """Test health check endpoints."""
        chat_health = chatbot_client.get('/health')
        assert chat_health.status_code == 200
        assert json.loads(chat_health.data)['status'] == 'ok'
        
        rag_health = rag_client.get('/health')
        assert rag_health.status_code == 200
        assert json.loads(rag_health.data)['status'] == 'ok'
    
    def test_concurrent_operations(self, chatbot_client, rag_client):
        """Test concurrent operations on different systems."""
        # Chat
        chat_resp = chatbot_client.post('/chat', json={'message': 'Hello'})
        
        # RAG
        rag_resp = rag_client.post('/query', json={'query': 'test'})
        
        assert chat_resp.status_code == 200
        assert rag_resp.status_code == 200
