"""Aspect-based sentiment analysis module."""
from typing import Dict, List, Tuple, Optional


class AspectSentimentAnalyzer:
    """Analyze sentiment for specific aspects/attributes."""
    
    def __init__(self):
        """Initialize aspect sentiment analyzer."""
        # Common aspects and their associated keywords
        self.aspects = {
            'quality': ['quality', 'build', 'durability', 'sturdy', 'robust', 'solid', 'crafted'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'affordable', 'value', 'money'],
            'performance': ['performance', 'speed', 'fast', 'slow', 'efficient', 'works', 'runs'],
            'design': ['design', 'look', 'appearance', 'style', 'aesthetic', 'beautiful', 'ugly'],
            'usability': ['easy', 'difficult', 'usable', 'intuitive', 'complex', 'simple', 'friendly'],
            'customer_service': ['service', 'support', 'customer', 'helpful', 'responsive', 'care'],
            'delivery': ['delivery', 'shipping', 'arrived', 'package', 'fast', 'slow', 'on-time'],
            'reliability': ['reliable', 'consistent', 'depends', 'dependable', 'breaks', 'fails']
        }
        
        # Positive and negative words
        self.positive_words = {
            'excellent': 1.0, 'great': 0.9, 'good': 0.7, 'amazing': 1.0,
            'love': 0.9, 'perfect': 1.0, 'fantastic': 0.95, 'wonderful': 0.9,
            'best': 0.95, 'awesome': 0.95, 'nice': 0.7, 'beautiful': 0.8,
            'fast': 0.7, 'easy': 0.7, 'simple': 0.6, 'helpful': 0.8,
            'satisfied': 0.8, 'happy': 0.8, 'impressed': 0.85
        }
        
        self.negative_words = {
            'terrible': -1.0, 'awful': -1.0, 'bad': -0.7, 'horrible': -0.95,
            'hate': -0.95, 'poor': -0.8, 'broken': -0.95, 'useless': -1.0,
            'worst': -1.0, 'disappointing': -0.85, 'slow': -0.7, 'complicated': -0.7,
            'difficult': -0.6, 'unhappy': -0.8, 'regret': -0.85, 'waste': -0.9
        }
    
    def analyze_aspect(self, text: str, aspect: str) -> Dict[str, object]:
        """Analyze sentiment for a specific aspect.

        Args:
            text: Text to analyze.
            aspect: Aspect to analyze (e.g., 'quality', 'price').

        Returns:
            Dict with keys: 'aspect', 'sentiment', 'score'.
        """
        text_lower = text.lower()

        # Check if aspect is mentioned
        aspect_keywords = self.aspects.get(aspect.lower(), [])
        aspect_mentioned = any(keyword in text_lower for keyword in aspect_keywords)

        if not aspect_mentioned:
            return {'aspect': aspect, 'sentiment': 'not_mentioned', 'score': 0.0}

        # Calculate sentiment for this aspect
        score = 0.0
        word_count = 0

        for word, weight in self.positive_words.items():
            if word in text_lower:
                score += weight
                word_count += 1

        for word, weight in self.negative_words.items():
            if word in text_lower:
                score += weight
                word_count += 1

        if word_count == 0:
            # Heuristic fallback: check for common aspect modifiers when no explicit sentiment words found
            if aspect.lower() == 'price':
                if 'expensive' in text_lower or 'too high' in text_lower or 'overpriced' in text_lower or 'pricey' in text_lower:
                    return {'aspect': aspect, 'sentiment': 'negative', 'score': -0.8}
                if 'cheap' in text_lower or 'affordable' in text_lower or 'reasonable' in text_lower:
                    return {'aspect': aspect, 'sentiment': 'positive', 'score': 0.8}
            return {'aspect': aspect, 'sentiment': 'neutral', 'score': 0.0}

        avg_score = score / word_count
        if avg_score > 0.3:
            sentiment = 'positive'
            final_score = min(avg_score, 1.0)
        elif avg_score < -0.3:
            sentiment = 'negative'
            final_score = max(avg_score, -1.0)
        else:
            sentiment = 'neutral'
            final_score = avg_score

        return {'aspect': aspect, 'sentiment': sentiment, 'score': final_score}
    
    def analyze_all_aspects(self, text: str) -> Dict[str, Dict]:
        """Analyze sentiment for all aspects in text.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Dictionary with analysis for each aspect.
        """
        results = {}
        
        for aspect in self.aspects.keys():
            aspect_result = self.analyze_aspect(text, aspect)
            if aspect_result and aspect_result.get('sentiment') != 'not_mentioned':
                results[aspect] = {
                    'sentiment': aspect_result.get('sentiment'),
                    'score': aspect_result.get('score')
                }
        
        return results
    
    def get_aspect_keywords(self, aspect: str, polarity: str = None) -> List[str]:
        """Get keywords associated with an aspect.

        Args:
            aspect: Aspect name.
            polarity: Optional 'positive' or 'negative' to filter keywords.

        Returns:
            List of keywords.
        """
        base = self.aspects.get(aspect.lower(), [])
        if polarity is None:
            return base
        # Return intersection when possible; otherwise return top sentiment words
        if polarity == 'positive':
            intersect = [w for w in base if w in self.positive_words]
            return intersect if intersect else list(self.positive_words.keys())
        if polarity == 'negative':
            intersect = [w for w in base if w in self.negative_words]
            return intersect if intersect else list(self.negative_words.keys())
        return base
    
    def list_aspects(self) -> List[str]:
        """Get list of supported aspects.
        
        Returns:
            List of aspect names.
        """
        return list(self.aspects.keys())
