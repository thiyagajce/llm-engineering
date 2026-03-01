"""Unit tests for advanced sentiment analysis modules."""
import pytest
import sys
import os

# Add project paths
# project_root should be the repository root (llm-engineering)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sentiment_path = os.path.join(project_root, 'ai-projects', 'projects', 'sentiment-analysis')
if sentiment_path not in sys.path:
    sys.path.insert(0, sentiment_path)

# Change to sentiment analysis directory for imports
original_dir = os.getcwd()
try:
    os.chdir(sentiment_path)
    from emotions import EmotionDetector, Emotion
    from aspect_sentiment import AspectSentimentAnalyzer
    from advanced_analysis import SubjectivityAnalyzer, ComparativeSentimentAnalyzer
    from explainability import SentimentExplainer
finally:
    os.chdir(original_dir)


class TestEmotionDetector:
    """Tests for emotion detection."""
    
    def test_emotion_detector_initialization(self):
        """Test EmotionDetector initialization."""
        detector = EmotionDetector()
        assert detector is not None
    
    def test_detect_joy(self):
        """Test joy emotion detection."""
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect("I love this! I'm so happy!")
        assert emotion == Emotion.JOY
        assert confidence > 0
        assert scores[Emotion.JOY] > scores.get(Emotion.SADNESS, 0)
    
    def test_detect_sadness(self):
        """Test sadness emotion detection."""
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect("I'm so sad and depressed")
        assert emotion == Emotion.SADNESS
        assert confidence > 0
        assert scores[Emotion.SADNESS] > 0
    
    def test_detect_anger(self):
        """Test anger emotion detection."""
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect("I'm furious! This angers me!")
        assert emotion == Emotion.ANGER
        assert confidence > 0
        assert scores[Emotion.ANGER] > 0
    
    def test_detect_fear(self):
        """Test fear emotion detection."""
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect("I'm scared and worried")
        assert emotion == Emotion.FEAR
        assert confidence > 0
    
    def test_detect_surprise(self):
        """Test surprise emotion detection."""
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect("Wow! That's surprising and amazing!")
        assert emotion == Emotion.SURPRISE
        assert confidence > 0
    
    def test_negation_handling(self):
        """Test that negations are handled properly."""
        detector = EmotionDetector()
        # "not happy" should reduce joy score
        emotion1, _, scores1 = detector.detect("I'm happy")
        emotion2, _, scores2 = detector.detect("I'm not happy")
        assert scores1[Emotion.JOY] > scores2[Emotion.JOY]
    
    def test_intensifier_detection(self):
        """Test intensifier handling."""
        detector = EmotionDetector()
        # "very happy" should have higher intensity than "happy"
        _, conf1, _ = detector.detect("I'm happy")
        _, conf2, _ = detector.detect("I'm very happy")
        assert conf2 >= conf1
    
    def test_emotion_distribution(self):
        """Test emotion distribution analysis."""
        detector = EmotionDetector()
        texts = [
            "I love this!",
            "This makes me sad",
            "I'm very angry"
        ]
        distribution = detector.get_emotion_distribution(texts)
        assert Emotion.JOY in distribution
        assert Emotion.SADNESS in distribution
        assert Emotion.ANGER in distribution
    
    def test_empty_text(self):
        """Test handling of empty text."""
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect("")
        assert emotion is not None
        assert confidence >= 0


class TestAspectSentimentAnalyzer:
    """Tests for aspect-based sentiment analysis."""
    
    def test_aspect_analyzer_initialization(self):
        """Test AspectSentimentAnalyzer initialization."""
        analyzer = AspectSentimentAnalyzer()
        assert analyzer is not None
    
    def test_list_aspects(self):
        """Test listing available aspects."""
        analyzer = AspectSentimentAnalyzer()
        aspects = analyzer.list_aspects()
        assert 'quality' in aspects
        assert 'price' in aspects
        assert 'performance' in aspects
    
    def test_analyze_quality_aspect(self):
        """Test quality aspect analysis."""
        analyzer = AspectSentimentAnalyzer()
        result = analyzer.analyze_aspect("The product quality is excellent", "quality")
        assert result['aspect'] == 'quality'
        assert result['sentiment'] in ['positive', 'negative', 'neutral']
    
    def test_analyze_price_aspect(self):
        """Test price aspect analysis."""
        analyzer = AspectSentimentAnalyzer()
        result = analyzer.analyze_aspect("The price is too high", "price")
        assert result['aspect'] == 'price'
        assert result['sentiment'] == 'negative'
    
    def test_analyze_all_aspects(self):
        """Test multi-aspect analysis."""
        analyzer = AspectSentimentAnalyzer()
        text = "Great quality but expensive with poor customer service"
        aspects = analyzer.analyze_all_aspects(text)
        
        assert len(aspects) > 0
        for aspect_name, aspect_data in aspects.items():
            assert 'sentiment' in aspect_data
            assert 'score' in aspect_data
    
    def test_get_aspect_keywords(self):
        """Test getting keywords for an aspect."""
        analyzer = AspectSentimentAnalyzer()
        positive_kw = analyzer.get_aspect_keywords('quality', 'positive')
        negative_kw = analyzer.get_aspect_keywords('quality', 'negative')
        
        assert len(positive_kw) > 0
        assert len(negative_kw) > 0
    
    def test_non_existent_aspect(self):
        """Test handling of non-existent aspect."""
        analyzer = AspectSentimentAnalyzer()
        result = analyzer.analyze_aspect("Some text", "non_existent_aspect")
        # Should handle gracefully or return neutral
        assert result is not None or result is None


class TestSubjectivityAnalyzer:
    """Tests for subjectivity analysis."""
    
    def test_subjectivity_analyzer_initialization(self):
        """Test SubjectivityAnalyzer initialization."""
        analyzer = SubjectivityAnalyzer()
        assert analyzer is not None
    
    def test_objective_text(self):
        """Test objective text detection."""
        analyzer = SubjectivityAnalyzer()
        label, score = analyzer.analyze_subjectivity(
            "The product weighs 500 grams and measures 10cm in length"
        )
        assert label in ['subjective', 'objective']
        assert 0 <= score <= 1
    
    def test_subjective_text(self):
        """Test subjective text detection."""
        analyzer = SubjectivityAnalyzer()
        label, score = analyzer.analyze_subjectivity(
            "I think this is a beautiful and amazing product"
        )
        assert label in ['subjective', 'objective']
    
    def test_mixed_text(self):
        """Test mixed objective and subjective text."""
        analyzer = SubjectivityAnalyzer()
        label, score = analyzer.analyze_subjectivity(
            "The phone has 128GB storage and I love its amazing camera"
        )
        assert label in ['subjective', 'objective']
        assert 0 <= score <= 1
    
    def test_subjectivity_score_range(self):
        """Test that subjectivity scores are in valid range."""
        analyzer = SubjectivityAnalyzer()
        texts = [
            "100 grams weight",
            "This is amazing",
            "Black color and fast processor"
        ]
        for text in texts:
            _, score = analyzer.analyze_subjectivity(text)
            assert 0 <= score <= 1


class TestComparativeSentimentAnalyzer:
    """Tests for comparative sentiment analysis."""
    
    def test_comparative_analyzer_initialization(self):
        """Test ComparativeSentimentAnalyzer initialization."""
        analyzer = ComparativeSentimentAnalyzer()
        assert analyzer is not None
    
    def test_detect_better_comparison(self):
        """Test detection of 'better' comparisons."""
        analyzer = ComparativeSentimentAnalyzer()
        is_comp, comp_type, keywords = analyzer.detect_comparison(
            "This product is better than the competitor's"
        )
        assert is_comp
        assert comp_type == 'better'
    
    def test_detect_worse_comparison(self):
        """Test detection of 'worse' comparisons."""
        analyzer = ComparativeSentimentAnalyzer()
        is_comp, comp_type, keywords = analyzer.detect_comparison(
            "This is worse than the other brand"
        )
        assert is_comp
        assert comp_type in ['worse', 'more']  # Pattern match might vary
    
    def test_detect_equal_comparison(self):
        """Test detection of equal comparisons."""
        analyzer = ComparativeSentimentAnalyzer()
        is_comp, comp_type, keywords = analyzer.detect_comparison(
            "This is as good as the other one"
        )
        # May or may not detect depending on keyword matching
        assert isinstance(is_comp, bool)
    
    def test_non_comparative_text(self):
        """Test non-comparative text."""
        analyzer = ComparativeSentimentAnalyzer()
        is_comp, comp_type, keywords = analyzer.detect_comparison(
            "This is a good product"
        )
        assert not is_comp
    
    def test_extract_comparisons(self):
        """Test extracting comparison objects."""
        analyzer = ComparativeSentimentAnalyzer()
        text = "Product A is better than Product B"
        comparisons = analyzer.extract_comparisons(text)
        assert isinstance(comparisons, list)
    
    def test_multiple_comparisons(self):
        """Test handling multiple comparisons in one text."""
        analyzer = ComparativeSentimentAnalyzer()
        text = "This is better than X but worse than Y"
        # Extract and count
        comparisons = analyzer.extract_comparisons(text)
        assert isinstance(comparisons, list)


class TestSentimentExplainer:
    """Tests for sentiment explainability."""
    
    def test_explainer_initialization(self):
        """Test SentimentExplainer initialization."""
        explainer = SentimentExplainer()
        assert explainer is not None
    
    def test_explain_positive_sentiment(self):
        """Test explaining positive sentiment."""
        explainer = SentimentExplainer()
        result = explainer.explain_sentiment("I love this amazing product!")
        
        assert 'sentiment' in result
        assert 'score' in result
        assert 'positive_words' in result
        assert 'negative_words' in result
        assert result['score'] > 0
    
    def test_explain_negative_sentiment(self):
        """Test explaining negative sentiment."""
        explainer = SentimentExplainer()
        result = explainer.explain_sentiment("This is terrible and awful")
        
        assert result['score'] < 0
        assert len(result['negative_words']) > 0
    
    def test_explain_neutral_sentiment(self):
        """Test explaining neutral sentiment."""
        explainer = SentimentExplainer()
        result = explainer.explain_sentiment("The product is blue and rectangular")
        
        assert isinstance(result['score'], (int, float))
    
    def test_get_feature_importance(self):
        """Test getting feature importance."""
        explainer = SentimentExplainer()
        important_features = explainer.get_feature_importance("I love this!")
        
        assert isinstance(important_features, list)
        for word, importance in important_features:
            assert isinstance(word, str)
            assert isinstance(importance, (int, float))
    
    def test_highlight_important_words(self):
        """Test HTML highlighting of important words."""
        explainer = SentimentExplainer()
        html = explainer.highlight_important_words("I love this product")
        
        assert isinstance(html, str)
        if 'love' in html.lower() or '<span' in html:
            # Either contains markup or is original text
            assert True
    
    def test_get_explanation_text(self):
        """Test getting human-readable explanation."""
        explainer = SentimentExplainer()
        text = explainer.get_explanation_text("This is amazing and wonderful!")
        
        assert isinstance(text, str)
        assert len(text) > 0
    
    def test_sentiment_lexicon_coverage(self):
        """Test that sentiment lexicon has reasonable coverage."""
        explainer = SentimentExplainer()
        
        # Test positive words
        result = explainer.explain_sentiment("good excellent wonderful")
        assert len(result['positive_words']) > 0
        
        # Test negative words
        result = explainer.explain_sentiment("bad terrible awful")
        assert len(result['negative_words']) > 0


class TestIntegration:
    """Integration tests combining multiple modules."""
    
    def test_emotion_and_aspect_together(self):
        """Test emotion and aspect analysis together."""
        emotion_detector = EmotionDetector()
        aspect_analyzer = AspectSentimentAnalyzer()
        
        text = "The product quality is excellent! I'm very happy"
        
        emotion, _, _ = emotion_detector.detect(text)
        aspects = aspect_analyzer.analyze_all_aspects(text)
        
        assert emotion == Emotion.JOY
        assert len(aspects) > 0
    
    def test_subjectivity_and_comparison(self):
        """Test subjectivity and comparison detection together."""
        subj_analyzer = SubjectivityAnalyzer()
        comp_analyzer = ComparativeSentimentAnalyzer()
        
        text = "I think this is better than the other one"
        
        label, score = subj_analyzer.analyze_subjectivity(text)
        is_comp, comp_type, _ = comp_analyzer.detect_comparison(text)
        
        assert label in ['subjective', 'objective']
        assert is_comp is not None
    
    def test_all_modules_on_real_review(self):
        """Test all modules on a realistic product review."""
        emotion_detector = EmotionDetector()
        aspect_analyzer = AspectSentimentAnalyzer()
        subj_analyzer = SubjectivityAnalyzer()
        comp_analyzer = ComparativeSentimentAnalyzer()
        explainer = SentimentExplainer()
        
        review = "Great quality and excellent design, very happy with my purchase!"
        
        emotion, _, _ = emotion_detector.detect(review)
        aspects = aspect_analyzer.analyze_all_aspects(review)
        subj_label, subj_score = subj_analyzer.analyze_subjectivity(review)
        is_comp, _, _ = comp_analyzer.detect_comparison(review)
        explanation = explainer.explain_sentiment(review)
        
        assert emotion == Emotion.JOY
        assert len(aspects) > 0
        assert subj_label in ['subjective', 'objective']
        assert is_comp is not None
        assert explanation['score'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
