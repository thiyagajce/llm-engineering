"""Emotion detection module for sentiment analysis."""
from typing import Tuple, Dict, List
from enum import Enum


class Emotion(Enum):
    """Emotion types."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"


class EmotionDetector:
    """Detect emotions in text beyond basic sentiment."""
    
    def __init__(self):
        """Initialize emotion detector with emotion keywords."""
        self.emotion_keywords = {
            Emotion.JOY: [
                'love', 'amazing', 'wonderful', 'fantastic', 'excellent',
                'great', 'happy', 'joy', 'delighted', 'thrilled', 'awesome',
                'perfect', 'beautiful', 'good', 'nice', 'best', 'wonderful'
            ],
            Emotion.SADNESS: [
                'sad', 'unhappy', 'depressed', 'miserable', 'awful', 'terrible',
                'bad', 'horrible', 'disappointing', 'disappointed', 'down',
                'lonely', 'regret', 'sorrow', 'grief'
            ],
            Emotion.ANGER: [
                'angry', 'furious', 'rage', 'hate', 'despise', 'disgusting',
                'upset', 'irritated', 'annoyed', 'outraged', 'aggressive',
                'hostile', 'resentful', 'infuriated'
            ],
            Emotion.FEAR: [
                'afraid', 'scared', 'frightened', 'terrified', 'anxious',
                'worried', 'nervous', 'dread', 'horror', 'panic', 'nervous',
                'apprehensive', 'cautious', 'uneasy'
            ],
            Emotion.SURPRISE: [
                'surprised', 'shocked', 'amazed', 'unexpected', 'astonished',
                'wow', 'incredible', 'unbelievable', 'astounded', 'stunned',
                'taken aback', 'bewildered'
            ]
        }
        self.intensifiers = ['very', 'so', 'extremely', 'incredibly', 'absolutely']
        self.negators = ['not', 'no', 'never', 'neither']
    
    def detect(self, text: str) -> Tuple[Emotion, float, Dict[str, float]]:
        """Detect primary emotion and emotion scores.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Tuple of (primary_emotion, confidence, all_emotion_scores).
        """
        text_lower = text.lower()
        emotion_scores = {emotion: 0.0 for emotion in Emotion}

        # Check for intensifiers and negators
        has_intensifier = any(word in text_lower for word in self.intensifiers)
        intensity_boost = 1.3 if has_intensifier else 1.0
        has_negator = any(word in text_lower for word in self.negators)

        # Count emotion keywords and compute simple scores
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                # Base score scales with count and intensifiers
                score = count * intensity_boost
                if has_negator and emotion in [Emotion.JOY, Emotion.SURPRISE]:
                    score *= 0.5
                emotion_scores[emotion] = min(score, 1.0)

        # Small heuristic: prefer SURPRISE when explicit 'wow' or 'surprising' present
        if 'wow' in text_lower or 'surpris' in text_lower:
            emotion_scores[Emotion.SURPRISE] = max(emotion_scores.get(Emotion.SURPRISE, 0.0), 0.8)

        # Determine primary emotion
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[max_emotion]

        # Tie-breaker: if surprise is strong, prefer it over joy
        if emotion_scores.get(Emotion.SURPRISE, 0.0) >= 0.8 and emotion_scores.get(Emotion.JOY, 0.0) > 0:
            # reduce joy score to prefer surprise
            emotion_scores[Emotion.JOY] = emotion_scores[Emotion.JOY] * 0.4
            max_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = emotion_scores[max_emotion]

        if confidence == 0:
            primary_emotion = Emotion.NEUTRAL
            confidence = 0.0
        else:
            primary_emotion = max_emotion

        return primary_emotion, confidence, emotion_scores
    
    def get_emotion_distribution(self, texts: List[str]) -> Dict[Emotion, int]:
        """Get emotion distribution across multiple texts.
        
        Args:
            texts: List of texts to analyze.
            
        Returns:
            Dictionary with emotion counts.
        """
        distribution: Dict[Emotion, int] = {emotion: 0 for emotion in Emotion}
        for text in texts:
            emotion, _, _ = self.detect(text)
            distribution[emotion] += 1
        return distribution
