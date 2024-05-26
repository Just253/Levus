from flask import Blueprint, request, jsonify
from api.functions.interactions import get_response_from_openai

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    messages = request.json.get('messages')
    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    response = get_response_from_openai(messages)
    return jsonify({'response': response})
