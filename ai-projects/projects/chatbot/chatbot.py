"""Chatbot module with conversational logic."""
import re
from typing import Dict, List, Tuple


class Chatbot:
    """Simple pattern-based chatbot."""
    
    def __init__(self):
        """Initialize the chatbot with predefined responses."""
        self.patterns: List[Tuple[str, List[str]]] = [
            (r'hello|hi|greetings', [
                'Hello! How can I help you today?',
                'Hi there! What can I do for you?',
                'Greetings! How may I assist you?'
            ]),
            (r'how are you', [
                'I\'m doing great, thanks for asking!',
                'I\'m functioning well, how about you?',
                'All systems operational!'
            ]),
            (r'what is your name|who are you', [
                'I\'m a chatbot created to help you.',
                'You can call me ChatBot.',
                'I\'m an AI assistant.'
            ]),
            (r'bye|goodbye|see you', [
                'Goodbye! Have a great day!',
                'See you soon!',
                'Bye! Hope I could help.'
            ]),
            (r'thank you|thanks', [
                'You\'re welcome!',
                'Happy to help!',
                'My pleasure!'
            ]),
            (r'help|what can you do', [
                'I can chat with you, answer questions, and have conversations.',
                'I can help with general conversation and information retrieval.',
                'You can ask me anything and I\'ll do my best to help!'
            ]),
        ]
        self.conversation_history: List[Dict[str, str]] = []
    
    def respond(self, user_message: str) -> str:
        """Generate a response to user input.
        
        Args:
            user_message: The user's input message.
            
        Returns:
            A response from the chatbot.
        """
        # Store in history
        self.conversation_history.append({
            'user': user_message,
            'timestamp': len(self.conversation_history)
        })
        
        # Check patterns
        user_lower = user_message.lower()
        for pattern, responses in self.patterns:
            if re.search(pattern, user_lower):
                import random
                response = random.choice(responses)
                self.conversation_history[-1]['bot'] = response
                return response
        
        # Default response
        default_response = f"I understand you said: '{user_message}'. Can you tell me more?"
        self.conversation_history[-1]['bot'] = default_response
        return default_response
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
