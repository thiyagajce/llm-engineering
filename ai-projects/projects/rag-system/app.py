from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/query', methods=['POST'])
def query():
    data = request.json or {}
    q = data.get('query', '')
    # Placeholder retrieval + generation
    return jsonify({'answer': f"(RAG placeholder) Answer for: {q}"})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
