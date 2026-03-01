"""Enhanced chatbot with intent classification."""
import re
from typing import Dict, List, Tuple, Optional
from enum import Enum


class Intent(Enum):
    """Intent types."""
    GREETING = "greeting"
    GOODBYE = "goodbye"
    HELP = "help"
    QUESTION = "question"
    AFFIRMATION = "affirmation"
    NEGATION = "negation"
    UNKNOWN = "unknown"


class IntentClassifier:
    """Simple intent classifier based on keywords and patterns."""
    
    def __init__(self):
        """Initialize intent classifier."""
        self.patterns = {
            Intent.GREETING: r'\b(hello|hi|hey|greetings|howdy|good morning|good afternoon|good evening)\b',
            Intent.GOODBYE: r'\b(bye|goodbye|see you|farewell|bye bye|see you later)\b',
            Intent.HELP: r'\b(help|what can you do|assist|support|aid)\b',
            Intent.AFFIRMATION: r'\b(yes|yeah|yep|sure|okay|ok|agreed|correct|true)\b',
            Intent.NEGATION: r'\b(no|nope|nah|never|not|false|incorrect|disagree)\b',
        }
    
    def classify(self, text: str) -> Tuple[Intent, float]:
        """Classify user intent.
        
        Args:
            text: User input text.
            
        Returns:
            Tuple of (intent, confidence).
        """
        text_lower = text.lower()
        
        # Check for question marks
        is_question = '?' in text
        
        for intent, pattern in self.patterns.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                confidence = 0.9
                return intent, confidence
        
        # Default to question if it has question mark
        if is_question:
            return Intent.QUESTION, 0.7
        
        return Intent.UNKNOWN, 0.5


class EnhancedChatbot:
    """Enhanced chatbot with intent classification."""
    
    def __init__(self):
        """Initialize the enhanced chatbot."""
        self.intent_classifier = IntentClassifier()
        self.patterns: Dict[Intent, List[str]] = {
            Intent.GREETING: [
                'Hello! How can I help you today?',
                'Hi there! What can I do for you?',
                'Greetings! How may I assist you?',
                'Welcome! What brings you here?'
            ],
            Intent.GOODBYE: [
                'Goodbye! Have a great day!',
                'See you soon!',
                'Bye! Hope I could help.',
                'Take care!'
            ],
            Intent.HELP: [
                'I can chat with you, answer questions, and have conversations.',
                'I can help with general conversation and information.',
                'You can ask me anything and I\'ll do my best to help!',
                'I\'m here to assist with conversation and information.'
            ],
            Intent.QUESTION: [
                'That\'s a great question!',
                'Let me think about that...',
                'I\'d be happy to help with that.',
                'That\'s an interesting question.'
            ],
            Intent.AFFIRMATION: [
                'Great! I agree with you.',
                'Absolutely!',
                'You\'re right on that.',
                'Couldn\'t agree more!'
            ],
            Intent.NEGATION: [
                'I understand. Let\'s move on.',
                'No problem. What else can I help with?',
                'Got it. Anything else?',
                'Okay, I see your point.'
            ],
            Intent.UNKNOWN: [
                'I understand you said: "{text}". Can you tell me more?',
                'Interesting! Could you elaborate?',
                'I see. Tell me more about that.',
                'That\'s noted. What else?'
            ]
        }
        self.conversation_history: List[Dict[str, str]] = []
    
    def respond(self, user_message: str) -> Dict[str, str]:
        """Generate a response with intent classification.
        
        Args:
            user_message: The user's input message.
            
        Returns:
            Dictionary with response and metadata.
        """
        # Classify intent
        intent, confidence = self.intent_classifier.classify(user_message)
        
        # Get response
        import random
        responses = self.patterns.get(intent, self.patterns[Intent.UNKNOWN])
        response_template = random.choice(responses)
        
        # Format response
        if '{text}' in response_template:
            response = response_template.format(text=user_message)
        else:
            response = response_template
        
        # Store in history
        self.conversation_history.append({
            'user': user_message,
            'bot': response,
            'intent': intent.value,
            'confidence': confidence,
            'turn': len(self.conversation_history)
        })
        
        return {
            'reply': response,
            'intent': intent.value,
            'confidence': confidence,
            'turn': len(self.conversation_history)
        }
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_intent_stats(self) -> Dict[str, int]:
        """Get statistics on identified intents."""
        stats = {}
        for entry in self.conversation_history:
            intent = entry['intent']
            stats[intent] = stats.get(intent, 0) + 1
        return stats
