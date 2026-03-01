"""Sentiment analysis module with TF-IDF and Logistic Regression."""
import pickle
from pathlib import Path
from typing import List, Tuple, Optional


class SentimentAnalyzer:
    """Sentiment analysis using scikit-learn."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.vectorizer = None
        self.model = None
        self.is_trained = False
    
    def train(self, texts: List[str], labels: List[int]) -> None:
        """Train the sentiment analysis model.
        
        Args:
            texts: List of text samples.
            labels: List of sentiment labels (0=negative, 1=positive).
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
        except ImportError:
            raise ImportError("scikit-learn is required for sentiment analysis")
        
        if len(texts) != len(labels):
            raise ValueError("Number of texts and labels must match")
        
        # Train vectorizer
        self.vectorizer = TfidfVectorizer(max_features=1000, lowercase=True, stop_words='english')
        X = self.vectorizer.fit_transform(texts)
        
        # Train model
        self.model = LogisticRegression(max_iter=200, random_state=42)
        self.model.fit(X, labels)
        
        self.is_trained = True
    
    def predict(self, text: str) -> Tuple[int, float]:
        """Predict sentiment of a text.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Tuple of (prediction, confidence).
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.vectorizer.transform([text])
        prediction = self.model.predict(X)[0]
        confidence = max(self.model.predict_proba(X)[0])
        
        return int(prediction), float(confidence)
    
    def predict_batch(self, texts: List[str]) -> List[Tuple[int, float]]:
        """Predict sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze.
            
        Returns:
            List of (prediction, confidence) tuples.
        """
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
    
    def save_model(self, path: Path) -> None:
        """Save trained model to file.
        
        Args:
            path: Path to save model.
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        with open(path, 'wb') as f:
            pickle.dump((self.vectorizer, self.model), f)
    
    def load_model(self, path: Path) -> None:
        """Load trained model from file.
        
        Args:
            path: Path to load model from.
        """
        with open(path, 'rb') as f:
            self.vectorizer, self.model = pickle.load(f)
        self.is_trained = True
    
    def evaluate(self, texts: List[str], labels: List[int]) -> float:
        """Evaluate model accuracy on test data.
        
        Args:
            texts: Test texts.
            labels: True labels.
            
        Returns:
            Accuracy score.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        X = self.vectorizer.transform(texts)
        return float(self.model.score(X, labels))
