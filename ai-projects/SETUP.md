# AI Projects - Complete Setup & Usage Guide

## Overview

This project contains three complete AI systems with Flask backends and comprehensive testing:

1. **Chatbot** - Pattern-based conversational AI with intent classification
2. **Sentiment Analysis** - Machine learning-based sentiment classifier
3. **RAG System** - Retrieval-Augmented Generation for document-based QA

## Quick Start

### Prerequisites

- Python 3.8+
- Flask
- scikit-learn (optional, for sentiment analysis)

### Installation

```bash
# Install dependencies
pip install -r ai-projects/requirements.txt

# Optional: Install sklearn for full sentiment analysis features
pip install scikit-learn
```

### Running the Applications

#### Chatbot Server

```bash
cd ai-projects/projects/chatbot
python app.py
# Runs on http://localhost:5001
```

#### RAG System Server

```bash
cd ai-projects/projects/rag-system
python app.py
# Runs on http://localhost:5003
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_chatbot.py -v
pytest tests/test_rag_system.py -v
pytest tests/test_sentiment_analysis.py -v

# Run integration tests
pytest tests/test_integration.py -v
```

### Using the Dashboard

Open `ai-projects/dashboard.html` in your browser to interact with all systems visually.

## API Documentation

### Chatbot API (Port 5001)

#### POST /chat

Send a message to the chatbot.

**Request:**

```json
{
  "message": "Hello, how are you?"
}
```

**Response:**

```json
{
  "reply": "Hello! How can I help you today?",
  "intent": "greeting",
  "confidence": 0.9,
  "history_length": 1
}
```

#### GET /history

Get conversation history.

**Response:**

```json
{
  "history": [
    {
      "user": "Hello",
      "bot": "Hi there!",
      "intent": "greeting",
      "confidence": 0.9,
      "turn": 1
    }
  ]
}
```

#### POST /clear

Clear conversation history.

**Response:**

```json
{
  "status": "cleared"
}
```

### RAG System API (Port 5003)

#### POST /query

Query the RAG system.

**Request:**

```json
{
  "query": "What is machine learning?"
}
```

**Response:**

```json
{
  "query": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "documents_retrieved": 2,
  "retrieved_docs": [
    {
      "title": "ML Basics",
      "score": 0.85
    }
  ]
}
```

#### GET /documents

Get all loaded documents.

**Response:**

```json
{
  "count": 2,
  "documents": [
    {
      "title": "doc1",
      "preview": "This is a document preview..."
    }
  ]
}
```

### Sentiment Analysis Training

```bash
cd ai-projects/projects/sentiment-analysis

# Train model with default data
python train.py

# Train with custom CSV
python train.py --data path/to/data.csv --model-out model.pkl

# CSV Format
# text,label
# I love this!,1
# This is terrible,0
```

## Module Architecture

### Chatbot Module

- **File:** `chatbot.py` / `enhanced_chatbot.py`
- **Classes:** `Chatbot`, `EnhancedChatbot`, `IntentClassifier`
- **Features:**
  - Pattern-based response generation
  - Intent classification (greeting, question, help, etc.)
  - Conversation history tracking
  - Configurable response patterns

### Sentiment Analyzer Module

- **File:** `sentiment_analyzer.py`
- **Class:** `SentimentAnalyzer`
- **Features:**
  - TF-IDF vectorization
  - Logistic Regression based classification
  - Batch prediction
  - Model persistence (save/load)
  - Accuracy evaluation

### RAG System Module

- **File:** `rag_system.py`
- **Classes:** `DocumentStore`, `Retriever`, `RAGSystem`
- **Features:**
  - Document indexing and retrieval
  - Keyword-based search
  - Context-aware answer generation
  - Document loading from directories

## Testing

### Test Coverage

1. **Unit Tests** (`test_chatbot.py`, `test_rag_system.py`, `test_sentiment_analysis.py`)
   - Individual module functionality
   - Flask endpoint testing
   - Error handling

2. **Integration Tests** (`test_integration.py`)
   - Full conversation flows
   - Cross-system operations
   - Concurrent requests
   - Error recovery

### Running Tests

```bash
# All tests with verbose output
pytest tests/ -v

# Fast test run
pytest tests/ -q

# With coverage report
pytest tests/ --cov=ai-projects

# Specific test class
pytest tests/test_integration.py::TestChatbotIntegration -v
```

## Metrics & Monitoring

Track system performance with the metrics module:

```python
from src.llm_engineering.metrics import MetricsTracker, RequestLogger

tracker = MetricsTracker()
logger = RequestLogger(tracker)

# Log events
logger.log_request('chatbot', '/chat', 'POST', user_id='user123')
logger.log_response('chatbot', '/chat', 200, response_time=45.2)

# Get summary
summary = tracker.get_summary()
print(summary)

# Save metrics
tracker.save_metrics('metrics.json')
```

## Configuration

### Project Structure

```
ai-projects/
├── projects/
│   ├── chatbot/
│   │   ├── app.py              # Flask app
│   │   ├── chatbot.py          # Chatbot module
│   │   └── enhanced_chatbot.py # Enhanced with intent classification
│   ├── sentiment-analysis/
│   │   ├── app.py (if exists)
│   │   ├── sentiment_analyzer.py
│   │   └── train.py            # Training script
│   └── rag-system/
│       ├── app.py              # Flask app
│       └── rag_system.py        # RAG system module
├── datasets/
│   ├── sentiment.csv           # Sample sentiment data
│   └── docs/                   # Sample documents
├── requirements.txt            # Python dependencies
└── dashboard.html              # Web interface
```

### Environment Variables

No special environment variables are required. Apps use default ports:

- Chatbot: `5001`
- RAG System: `5003`

## Troubleshooting

### Issue: ImportError for sklearn

**Solution:** Install scikit-learn

```bash
pip install scikit-learn
```

### Issue: Port already in use

**Solution:** Change port in app.py or kill existing process

```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

### Issue: Cannot load documents

**Solution:** Ensure documents are in `datasets/docs/` directory

```bash
mkdir -p ai-projects/datasets/docs
# Add .txt files to this directory
```

## Next Steps

- [ ] Add database integration (PostgreSQL)
- [ ] Implement semantic search with embeddings
- [ ] Add authentication/authorization
- [ ] Create admin dashboard for metrics
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add caching for RAG results
- [ ] Implement feedback system

## Contributing

1. Create feature branch
2. Add tests for new features
3. Update documentation
4. Commit and push
5. Create pull request

## License

See LICENSE file in repository root.
