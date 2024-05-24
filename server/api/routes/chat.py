from flask import Blueprint, request, jsonify
from openai import GPT4
#from api.functions import interactions

chat_bp = Blueprint('chat', __name__)

# gpt4 = GPT4('APIKEY')
@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('Mensaje | Input: ', '')
    response = GPT4.generate(user_input)
    return jsonify({'Levus | Output ': response})