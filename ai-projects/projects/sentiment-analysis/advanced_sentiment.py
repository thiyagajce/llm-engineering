"""Comprehensive advanced sentiment analyzer combining all features."""
from typing import Dict, Any
from sentiment_analyzer import SentimentAnalyzer
from emotions import EmotionDetector
from aspect_sentiment import AspectSentimentAnalyzer
from advanced_analysis import SubjectivityAnalyzer, ComparativeSentimentAnalyzer
from explainability import SentimentExplainer


class AdvancedSentimentAnalyzer:
    """Advanced sentiment analyzer with multiple analysis dimensions."""
    
    def __init__(self):
        """Initialize advanced sentiment analyzer with all components."""
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_detector = EmotionDetector()
        self.aspect_analyzer = AspectSentimentAnalyzer()
        self.subjectivity_analyzer = SubjectivityAnalyzer()
        self.comparative_analyzer = ComparativeSentimentAnalyzer()
        self.explainer = SentimentExplainer()
    
    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """Comprehensive sentiment analysis of text.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Dictionary with all analysis dimensions.
        """
        # 1. Basic sentiment - try ML model, fallback to rule-based explainer if sklearn missing
        basic_label = 'neutral'
        basic_confidence = 0.0
        try:
            if not self.sentiment_analyzer.is_trained:
                texts = ["I love this!", "This is terrible", "Pretty good", "Worst ever"]
                labels = [1, 0, 1, 0]
                self.sentiment_analyzer.train(texts, labels)

            basic_sentiment, basic_confidence = self.sentiment_analyzer.predict(text)
            basic_label = 'positive' if basic_sentiment == 1 else 'negative'
        except Exception:
            # Fallback: use simple lexicon-based explainer
            explanation_fb = self.explainer.explain_sentiment(text)
            basic_label = explanation_fb.get('sentiment', 'neutral')
            # Normalize confidence to [0,1] from absolute score magnitude
            score_fb = explanation_fb.get('score', 0.0)
            basic_confidence = min(1.0, abs(score_fb) / 2.0)
        
        # 2. Emotion detection
        emotion, emotion_confidence, emotion_scores = self.emotion_detector.detect(text)
        
        # 3. Aspect-based sentiment
        aspects = self.aspect_analyzer.analyze_all_aspects(text)
        
        # 4. Subjectivity analysis
        subjectivity_label, subjectivity_score = self.subjectivity_analyzer.analyze_subjectivity(text)
        
        # 5. Comparative sentiment
        is_comparative, comparison_type, comparison_keywords = self.comparative_analyzer.detect_comparison(text)
        
        # 6. Explainability
        explanation = self.explainer.explain_sentiment(text)
        feature_importance = self.explainer.get_feature_importance(text)
        explanation_text = self.explainer.get_explanation_text(text)
        
        return {
            'text': text,
            'overall_analysis': {
                'sentiment': basic_label,
                'confidence': basic_confidence,
                'score': explanation['score']
            },
            'emotion_analysis': {
                'primary_emotion': emotion.value,
                'confidence': emotion_confidence,
                'emotion_scores': {e.value: emotion_scores[e] for e in emotion_scores}
            },
            'aspect_sentiment': aspects if aspects else {'no_aspects': 'detected'},
            'subjectivity': {
                'label': subjectivity_label,
                'score': subjectivity_score
            },
            'comparative_analysis': {
                'contains_comparison': is_comparative,
                'type': comparison_type if is_comparative else None,
                'keywords': comparison_keywords
            },
            'explainability': {
                'top_features': [{'word': word, 'importance': score} 
                               for word, score in feature_importance],
                'explanation': explanation_text,
                'positive_words': [word for word, _ in explanation['positive_words']],
                'negative_words': [word for word, _ in explanation['negative_words']]
            }
        }
    
    def batch_analyze(self, texts: list) -> list:
        """Analyze multiple texts in batch.
        
        Args:
            texts: List of texts to analyze.
            
        Returns:
            List of analysis results.
        """
        return [self.analyze_comprehensive(text) for text in texts]
    
    def generate_report(self, text: str) -> str:
        """Generate human-readable analysis report.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Formatted report string.
        """
        analysis = self.analyze_comprehensive(text)
        
        report = [
            "=" * 60,
            "ADVANCED SENTIMENT ANALYSIS REPORT",
            "=" * 60,
            f"\nText: {text[:100]}...\n",
            
            "1. OVERALL SENTIMENT:",
            f"   - Sentiment: {analysis['overall_analysis']['sentiment'].upper()}",
            f"   - Confidence: {analysis['overall_analysis']['confidence']:.2%}",
            f"   - Score: {analysis['overall_analysis']['score']:.3f}",
            
            "\n2. EMOTION DETECTION:",
            f"   - Primary Emotion: {analysis['emotion_analysis']['primary_emotion']}",
            f"   - Confidence: {analysis['emotion_analysis']['confidence']:.2%}",
            
            "\n3. ASPECT SENTIMENT:",
        ]
        
        if 'no_aspects' not in analysis['aspect_sentiment']:
            for aspect, data in analysis['aspect_sentiment'].items():
                report.append(f"   - {aspect}: {data['sentiment']} ({data['score']:.2f})")
        else:
            report.append("   - No specific aspects detected")
        
        report.extend([
            "\n4. TEXT SUBJECTIVITY:",
            f"   - Type: {analysis['subjectivity']['label']}",
            f"   - Score: {analysis['subjectivity']['score']:.2%}",
            
            "\n5. COMPARATIVE ANALYSIS:",
            f"   - Contains comparison: {analysis['comparative_analysis']['contains_comparison']}",
        ])
        
        if analysis['comparative_analysis']['contains_comparison']:
            report.append(f"   - Type: {analysis['comparative_analysis']['type']}")
            report.append(f"   - Keywords: {', '.join(analysis['comparative_analysis']['keywords'])}")
        
        report.extend([
            "\n6. KEY DRIVERS:",
            f"   {analysis['explainability']['explanation']}",
            
            "\n" + "=" * 60,
        ])
        
        return '\n'.join(report)
    
    def compare_texts(self, text1: str, text2: str) -> Dict:
        """Compare sentiment of two texts.
        
        Args:
            text1: First text.
            text2: Second text.
            
        Returns:
            Comparison dictionary.
        """
        analysis1 = self.analyze_comprehensive(text1)
        analysis2 = self.analyze_comprehensive(text2)
        
        return {
            'text1_sentiment': analysis1['overall_analysis']['sentiment'],
            'text2_sentiment': analysis2['overall_analysis']['sentiment'],
            'text1_score': analysis1['overall_analysis']['score'],
            'text2_score': analysis2['overall_analysis']['score'],
            'emotion1': analysis1['emotion_analysis']['primary_emotion'],
            'emotion2': analysis2['emotion_analysis']['primary_emotion'],
            'more_positive': 'text1' if analysis1['overall_analysis']['score'] > 
                            analysis2['overall_analysis']['score'] else 'text2',
            'score_difference': abs(analysis1['overall_analysis']['score'] - 
                                   analysis2['overall_analysis']['score'])
        }
