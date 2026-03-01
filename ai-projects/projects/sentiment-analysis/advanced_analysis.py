"""Subjectivity detection and comparative sentiment analysis."""
from typing import Tuple, List


class SubjectivityAnalyzer:
    """Analyze subjectivity vs objectivity of text."""
    
    def __init__(self):
        """Initialize subjectivity analyzer."""
        self.subjective_words = [
            'feel', 'believe', 'think', 'opinion', 'thought', 'perspective',
            'personal', 'subjective', 'bias', 'prejudice', 'favorite', 'prefer',
            'like', 'dislike', 'love', 'hate', 'beautiful', 'ugly', 'good', 'bad',
            'wonderful', 'terrible', 'amazing', 'awful', 'probably', 'likely',
            'maybe', 'perhaps', 'might', 'seem', 'appear', 'looks'
        ]
        
        self.objective_words = [
            'fact', 'data', 'study', 'research', 'statistic', 'measurement',
            'analysis', 'evidence', 'actual', 'real', 'verified', 'confirmed',
            'documented', 'official', 'according', 'report', 'result', 'finding',
            'conclude', 'demonstrate', 'show', 'prove', 'indicate', 'reveal',
            'measure', 'weight', 'height', 'size', 'number', 'percent'
        ]
    
    def analyze_subjectivity(self, text: str) -> Tuple[str, float]:
        """Analyze subjectivity of text.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Tuple of (label, subjectivity_score).
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        subjective_count = sum(1 for word in words if word in self.subjective_words)
        objective_count = sum(1 for word in words if word in self.objective_words)
        
        total_relevant = subjective_count + objective_count
        
        if total_relevant == 0:
            subjectivity_score = 0.5  # Neutral if no relevant words
        else:
            subjectivity_score = subjective_count / total_relevant
        
        # Simplify labels to either 'subjective' or 'objective'
        label = 'subjective' if subjectivity_score >= 0.5 else 'objective'
        return label, subjectivity_score


class ComparativeSentimentAnalyzer:
    """Detect comparative sentiment statements."""
    
    def __init__(self):
        """Initialize comparative sentiment analyzer."""
        self.comparative_patterns = {
            'better': ['better', 'superior', 'improved', 'upgrade'],
            'worse': ['worse', 'inferior', 'downgrade', 'decline'],
            'equal': ['same', 'equal', 'equivalent', 'identical', 'alike'],
            'more': ['more', 'additional', 'extra', 'increased', 'higher'],
            'less': ['less', 'fewer', 'reduced', 'lower', 'decreased']
        }
    
    def detect_comparison(self, text: str) -> Tuple[bool, str, List[str]]:
        """Detect if text contains comparative statements.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Tuple of (is_comparative, comparison_type, keywords_found).
        """
        text_lower = text.lower()
        found_keywords = []
        comparison_type = None
        
        for comp_type, keywords in self.comparative_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.append(keyword)
                    if comparison_type is None:
                        comparison_type = comp_type
        
        is_comparative = len(found_keywords) > 0
        comparison_type = comparison_type or 'unknown'
        
        return is_comparative, comparison_type, found_keywords
    
    def extract_comparisons(self, text: str, window_size: int = 10) -> List[str]:
        """Extract comparison phrases from text.
        
        Args:
            text: Text to analyze.
            window_size: Number of words around comparison keyword.
            
        Returns:
            List of extracted comparison phrases.
        """
        text_lower = text.lower()
        words = text.split()
        comparisons = []
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            for keywords in self.comparative_patterns.values():
                if word_lower in keywords:
                    # Extract window around the keyword
                    start = max(0, i - window_size)
                    end = min(len(words), i + window_size + 1)
                    phrase = ' '.join(words[start:end])
                    comparisons.append(phrase)
        
        return comparisons
