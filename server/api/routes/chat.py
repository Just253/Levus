from flask import Blueprint, request, jsonify
from api.functions.interactions import get_response_from_openai

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return jsonify({'error': 'GET method not allowed'}), 405
    data = request.get_json()
    messages = data.get('messages')
    model = data.get('model')
    if not messages:
        return jsonify({'error': 'No messages provided'}), 400
    
    if isinstance(model, list):
        model = model[0]
    response = get_response_from_openai(messages,model=model)
    return jsonify({'response': response})
