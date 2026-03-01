"""Tests for the RAG (Retrieval-Augmented Generation) system."""
import sys
import json
from pathlib import Path
import pytest

# Add projects to path
rag_dir = Path(__file__).parent.parent / 'ai-projects' / 'projects' / 'rag-system'
sys.path.insert(0, str(rag_dir))


@pytest.fixture
def rag_client():
    """Create a test client for the RAG system Flask app."""
    # Change to rag dir to ensure imports work
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(str(rag_dir))
        from app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    finally:
        os.chdir(old_cwd)


def test_rag_system_health(rag_client):
    """Test that the RAG system health endpoint is reachable."""
    response = rag_client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'


def test_rag_system_query_response(rag_client):
    """Test that the RAG system responds to a query."""
    payload = {'query': 'What is machine learning?'}
    response = rag_client.post('/query', json=payload, content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data
    assert 'machine learning' in data['answer'].lower()


def test_rag_system_empty_query(rag_client):
    """Test that RAG system handles empty queries gracefully."""
    payload = {}
    response = rag_client.post('/query', json=payload, content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data


def test_rag_system_query_with_special_chars(rag_client):
    """Test that RAG system handles special characters in queries."""
    payload = {'query': 'What are the best practices & tips?'}
    response = rag_client.post('/query', json=payload, content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data
