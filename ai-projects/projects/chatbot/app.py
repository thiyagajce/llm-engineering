from flask import Flask, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    message = data.get('message', '')
    
    if not message.strip():
        return jsonify({'reply': 'Please provide a message.', 'error': True})
    
    # Get chatbot response
    reply = chatbot.respond(message)
    
    return jsonify({
        'reply': reply,
        'history_length': len(chatbot.conversation_history)
    })

@app.route('/history', methods=['GET'])
def history():
    """Get conversation history."""
    return jsonify({'history': chatbot.get_history()})

@app.route('/clear', methods=['POST'])
def clear():
    """Clear conversation history."""
    chatbot.clear_history()
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
