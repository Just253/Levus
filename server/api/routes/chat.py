from flask import Blueprint, request, jsonify
from openai import GPT4
#from tests.voice.vosk import rec ## Change for future implementation
#from api.functions import interactions
# De interacciones hacer la peticion a la API de OpenAI
chat_bp = Blueprint('chat', __name__)

# gpt4 = GPT4('APIKEY')
@chat_bp.route('/chat', methods=['POST'])
def chat():
    # messages = request.json['messages']
    # model = request.json['model']
    # response = interactions.ask(messages, model)
    response = GPT4.generate(rec.result())
    
    return jsonify({"response": response})