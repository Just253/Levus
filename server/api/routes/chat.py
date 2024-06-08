from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_executor import Executor
from ...functions.interactions import get_response_from_openai
from ...functions.db import statusTable
import uuid

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
    process_id = str(uuid.uuid4())
    table = statusTable("processes", app)
    table.create_status(process_id)
    executor = Executor(app)
    executor.submit(get_response_from_openai, messages, process_id,table=table, model=model)
    return jsonify({'process_id': process_id})
