"""Explainability module for sentiment analysis - show important features."""
from typing import Dict, List, Tuple
import re


class SentimentExplainer:
    """Explain sentiment predictions by identifying important words."""
    
    def __init__(self):
        """Initialize sentiment explainer."""
        # Sentiment lexicons
        self.positive_lexicon = {
            'love': 0.9, 'amazing': 1.0, 'wonderful': 0.9, 'fantastic': 0.95,
            'excellent': 1.0, 'great': 0.85, 'good': 0.7, 'awesome': 0.95,
            'perfect': 1.0, 'beautiful': 0.8, 'best': 0.95, 'nice': 0.65,
            'happy': 0.8, 'delighted': 0.9, 'thrilled': 0.95, 'enjoyed': 0.8,
            'impressed': 0.85, 'satisfied': 0.8, 'recommend': 0.8, 'worth': 0.7
        }
        
        self.negative_lexicon = {
            'hate': -0.95, 'terrible': -1.0, 'awful': -1.0, 'horrible': -0.95,
            'bad': -0.75, 'poor': -0.8, 'worst': -1.0, 'disappointing': -0.85,
            'waste': -0.9, 'regret': -0.85, 'broken': -0.9, 'useless': -1.0,
            'never': -0.6, 'not': -0.5, 'no': -0.5, 'wrong': -0.7,
            'fail': -0.8, 'problem': -0.7, 'issue': -0.65, 'complaint': -0.7
        }
        
        self.intensifiers = {'very': 1.3, 'extremely': 1.4, 'absolutely': 1.3,
                            'so': 1.25, 'incredibly': 1.35, 'really': 1.2}
        self.negators = {'not': -1, 'no': -1, 'never': -1}
    
    def explain_sentiment(self, text: str) -> Dict:
        """Explain sentiment prediction with feature importance.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Dictionary with explanation details.
        """
        words = re.findall(r'\w+', text.lower())
        
        positive_words = []
        negative_words = []
        neutral_words = []
        
        for word in words:
            if word in self.positive_lexicon:
                positive_words.append((word, self.positive_lexicon[word]))
            elif word in self.negative_lexicon:
                negative_words.append((word, self.negative_lexicon[word]))
            else:
                neutral_words.append(word)
        
        # Calculate overall sentiment
        pos_score = sum(score for _, score in positive_words)
        neg_score = sum(score for _, score in negative_words)
        overall_score = pos_score + neg_score
        
        # Determine sentiment
        if overall_score > 0.1:
            sentiment = 'positive'
        elif overall_score < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Sort by importance
        all_sentiment_words = positive_words + negative_words
        all_sentiment_words.sort(key=lambda x: abs(x[1]), reverse=True)
        
        return {
            'sentiment': sentiment,
            'score': overall_score,
            'positive_words': sorted(positive_words, key=lambda x: x[1], reverse=True),
            'negative_words': sorted(negative_words, key=lambda x: x[1]),
            'top_features': all_sentiment_words[:5],
            'word_count': len(words),
            'sentiment_word_count': len(all_sentiment_words)
        }
    
    def get_feature_importance(self, text: str) -> List[Tuple[str, float]]:
        """Get feature importance ranking for sentiment.
        
        Args:
            text: Text to analyze.
            
        Returns:
            List of (word, importance_score) tuples.
        """
        explanation = self.explain_sentiment(text)
        return explanation['top_features']
    
    def highlight_important_words(self, text: str) -> str:
        """Create HTML highlighting important sentiment words.
        
        Args:
            text: Text to analyze.
            
        Returns:
            HTML with highlighted words.
        """
        words = text.split()
        highlighted = []
        
        for word in words:
            word_clean = re.sub(r'\W', '', word.lower())
            
            if word_clean in self.positive_lexicon:
                score = self.positive_lexicon[word_clean]
                color = f'rgba(0, 150, 0, {score})'  # Green for positive
                highlighted.append(f'<span style="background-color: {color}; padding: 2px;">{word}</span>')
            elif word_clean in self.negative_lexicon:
                score = abs(self.negative_lexicon[word_clean])
                color = f'rgba(255, 0, 0, {score})'  # Red for negative
                highlighted.append(f'<span style="background-color: {color}; padding: 2px;">{word}</span>')
            else:
                highlighted.append(word)
        
        return ' '.join(highlighted)
    
    def get_explanation_text(self, text: str) -> str:
        """Get human-readable explanation of sentiment.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Explanation text.
        """
        explanation = self.explain_sentiment(text)
        
        sentiment = explanation['sentiment']
        score = explanation['score']
        top_features = explanation['top_features'][:3]
        
        feature_text = ', '.join([f"'{word}'" for word, _ in top_features])
        
        explanation_parts = [
            f"This text is classified as {sentiment.upper()} (score: {score:.2f}).",
            f"The {sentiment} sentiment is primarily driven by the words: {feature_text}.",
            f"Out of {explanation['word_count']} total words, {explanation['sentiment_word_count']} "
            f"carry sentiment information."
        ]
        
        return ' '.join(explanation_parts)
