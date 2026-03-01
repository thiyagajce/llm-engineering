#!/usr/bin/env python3
"""Demo script showcasing all AI project features."""

import sys
from pathlib import Path


def demo_chatbot():
    """Demo the enhanced chatbot."""
    print("\n" + "="*60)
    print("🤖 CHATBOT DEMO - Enhanced with Intent Classification")
    print("="*60)
    
    chatbot_dir = Path(__file__).parent / 'ai-projects' / 'projects' / 'chatbot'
    sys.path.insert(0, str(chatbot_dir))
    
    from enhanced_chatbot import EnhancedChatbot
    
    bot = EnhancedChatbot()
    
    test_messages = [
        "Hello there!",
        "What can you do?",
        "That's great!",
        "I disagree with you",
        "Goodbye!",
        "Tell me about Python"
    ]
    
    print("\n📝 Testing bot with various intents:")
    for msg in test_messages:
        response = bot.respond(msg)
        print(f"\n  User: {msg}")
        print(f"  Intent: {response['intent']} (confidence: {response['confidence']:.0%})")
        print(f"  Bot: {response['reply']}")
    
    print(f"\n📊 Intent Statistics:")
    stats = bot.get_intent_stats()
    for intent, count in stats.items():
        print(f"  - {intent.capitalize()}: {count} message(s)")


def demo_rag():
    """Demo the RAG system."""
    print("\n" + "="*60)
    print("🔍 RAG SYSTEM DEMO - Retrieval-Augmented Generation")
    print("="*60)
    
    rag_dir = Path(__file__).parent / 'ai-projects' / 'projects' / 'rag-system'
    sys.path.insert(0, str(rag_dir))
    
    from rag_system import RAGSystem
    
    rag = RAGSystem()
    
    # Add sample documents
    rag.add_document(
        "Python Basics",
        "Python is a high-level programming language. It's known for its simplicity and readability."
    )
    rag.add_document(
        "Machine Learning",
        "Machine learning is a subset of artificial intelligence that focuses on learning from data."
    )
    rag.add_document(
        "Web Development",
        "Web development involves building websites and web applications using technologies like HTML, CSS, and JavaScript."
    )
    
    print(f"\n📚 Loaded {len(rag.store.documents)} sample documents")
    
    test_queries = [
        "What is Python?",
        "Tell me about machine learning",
        "How do I build websites?"
    ]
    
    print("\n❓ RAG System Responses:")
    for query in test_queries:
        result = rag.generate_answer(query)
        print(f"\n  Query: {query}")
        print(f"  Answer: {result['answer'][:100]}...")
        print(f"  Documents Used: {result['documents_retrieved']}")


def demo_metrics():
    """Demo the metrics module."""
    print("\n" + "="*60)
    print("📊 METRICS & LOGGING DEMO")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent / 'src'))
    from llm_engineering.metrics import MetricsTracker, RequestLogger
    
    tracker = MetricsTracker()
    logger = RequestLogger(tracker)
    
    # Log some sample events
    logger.log_request('chatbot', '/chat', 'POST', user_id='user123')
    logger.log_response('chatbot', '/chat', 200, response_time=45.2)
    logger.log_request('rag', '/query', 'POST', query='test')
    logger.log_response('rag', '/query', 200, docs_retrieved=3)
    logger.log_error('sentiment', 'ImportError', 'sklearn not installed')
    
    print("\n📈 Logged Events Summary:")
    summary = tracker.get_summary()
    print(f"  Total Events: {summary['total_events']}")
    print(f"  Systems Tracked: {list(summary['systems'].keys())}")
    
    for sys_name, sys_data in summary['systems'].items():
        print(f"\n  {sys_name.upper()}:")
        print(f"    Total: {sys_data['total']}")
        for event, count in sys_data['events'].items():
            print(f"    - {event}: {count}")


def demo_openapi():
    """Demo OpenAPI documentation."""
    print("\n" + "="*60)
    print("📖 API DOCUMENTATION")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent / 'src'))
    from llm_engineering.openapi import OPENAPI_SPEC
    
    print("\n✅ OpenAPI Spec Generated with:")
    print(f"  - Base Servers: {len(OPENAPI_SPEC['servers'])}")
    print(f"  - API Endpoints: {len(OPENAPI_SPEC['paths'])}")
    
    print("\n  Available Endpoints:")
    for path, methods in OPENAPI_SPEC['paths'].items():
        for method in methods.keys():
            print(f"    {method.upper():6} {path}")


def main():
    """Run all demos."""
    print("\n🚀 AI PROJECTS - COMPLETE FEATURE DEMO")
    print("=" * 60)
    
    try:
        demo_chatbot()
    except Exception as e:
        print(f"❌ Chatbot demo error: {e}")
    
    try:
        demo_rag()
    except Exception as e:
        print(f"❌ RAG demo error: {e}")
    
    try:
        demo_metrics()
    except Exception as e:
        print(f"❌ Metrics demo error: {e}")
    
    try:
        demo_openapi()
    except Exception as e:
        print(f"❌ OpenAPI demo error: {e}")
    
    print("\n" + "="*60)
    print("✨ Demo Complete!")
    print("\n📚 Next Steps:")
    print("  1. Start Flask apps: cd ai-projects/projects/[chatbot|rag-system] && python app.py")
    print("  2. Open dashboard: ai-projects/dashboard.html in your browser")
    print("  3. Run tests: pytest tests/ -v")
    print("  4. Read setup guide: ai-projects/SETUP.md")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
