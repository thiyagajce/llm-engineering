from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    message = data.get('message', '')
    # Placeholder response
    return jsonify({'reply': f"You said: {message}"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
