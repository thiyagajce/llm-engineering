"""RAG (Retrieval-Augmented Generation) system module."""
from pathlib import Path
from typing import List, Dict, Tuple
import re


class DocumentStore:
    """Simple document store for RAG system."""
    
    def __init__(self):
        """Initialize the document store."""
        self.documents: Dict[int, Dict[str, str]] = {}
        self.doc_id_counter = 0
    
    def add_document(self, title: str, content: str) -> int:
        """Add a document to the store.
        
        Args:
            title: Document title.
            content: Document content.
            
        Returns:
            Document ID.
        """
        doc_id = self.doc_id_counter
        self.documents[doc_id] = {'title': title, 'content': content}
        self.doc_id_counter += 1
        return doc_id
    
    def load_from_directory(self, directory: Path) -> int:
        """Load documents from a directory of text files.
        
        Args:
            directory: Path to directory with .txt files.
            
        Returns:
            Number of documents loaded.
        """
        count = 0
        for file_path in Path(directory).glob('*.txt'):
            try:
                content = file_path.read_text()
                title = file_path.stem
                self.add_document(title, content)
                count += 1
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        return count
    
    def get_document(self, doc_id: int) -> Dict[str, str]:
        """Get a document by ID."""
        return self.documents.get(doc_id, {})
    
    def get_all_documents(self) -> List[Dict[str, str]]:
        """Get all documents."""
        return list(self.documents.values())


class Retriever:
    """Simple keyword-based document retriever."""
    
    def __init__(self, document_store: DocumentStore):
        """Initialize the retriever.
        
        Args:
            document_store: The document store to search.
        """
        self.store = document_store
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, any]]:
        """Retrieve relevant documents for a query.
        
        Args:
            query: Search query.
            top_k: Number of top results to return.
            
        Returns:
            List of relevant documents with relevance scores.
        """
        query_terms = set(query.lower().split())
        results = []
        
        for doc_id, doc in self.store.documents.items():
            # Simple keyword matching
            content = doc['content'].lower()
            title = doc['title'].lower()
            
            # Count matching terms
            matches = sum(1 for term in query_terms if term in content or term in title)
            score = matches / len(query_terms) if query_terms else 0
            
            if score > 0:
                results.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'content': doc['content'][:200],  # First 200 chars
                    'score': score
                })
        
        # Sort by score and return top-k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]


class RAGSystem:
    """Retrieval-Augmented Generation system."""
    
    def __init__(self):
        """Initialize the RAG system."""
        self.store = DocumentStore()
        self.retriever = Retriever(self.store)
    
    def add_document(self, title: str, content: str) -> int:
        """Add a document to the system."""
        return self.store.add_document(title, content)
    
    def load_documents(self, directory: Path) -> int:
        """Load documents from directory."""
        return self.store.load_from_directory(directory)
    
    def generate_answer(self, query: str) -> Dict[str, any]:
        """Generate answer based on query and retrieved documents.
        
        Args:
            query: User query.
            
        Returns:
            Answer with retrieved context.
        """
        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(query, top_k=3)
        
        # Build context from retrieved documents
        context = " ".join([doc['content'] for doc in retrieved_docs])
        
        # Generate simple answer
        if retrieved_docs:
            answer = self._generate_answer_from_context(query, context)
        else:
            answer = "I couldn't find relevant information to answer your question."
        
        return {
            'query': query,
            'answer': answer,
            'retrieved_documents': retrieved_docs,
            'context_length': len(context)
        }
    
    def _generate_answer_from_context(self, query: str, context: str) -> str:
        """Generate answer from context (simplified).
        
        Args:
            query: The user's query.
            context: Retrieved context.
            
        Returns:
            Generated answer.
        """
        # Simple heuristic: find sentences containing query terms
        query_terms = set(query.lower().split())
        sentences = re.split(r'[.!?]+', context)
        
        relevant_sentences = []
        for sentence in sentences:
            if any(term in sentence.lower() for term in query_terms):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            answer = ". ".join(relevant_sentences[:2]) + "."
        else:
            answer = f"Based on the retrieved documents: {context[:150]}..."
        
        return answer.strip()
