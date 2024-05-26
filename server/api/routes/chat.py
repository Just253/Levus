from flask import Blueprint, request, jsonify
from api.functions.interactions import get_response_from_openai
from openai import GPT4

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = get_response_from_openai(user_message)
    return jsonify({'response': response})
