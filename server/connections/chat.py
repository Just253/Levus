from flask import jsonify
from flask import current_app as app
from flask_executor import Executor
from ..api.functions.interactions import get_response_from_openai
from ..api.functions.db import statusTable
from .. import socketio
from flask_socketio import emit
import uuid

@socketio.on('new_message')
def chat(data):
  messages = data.get('messages')
  model = data.get('model')
  if not messages:
    emit('error', {'error': 'No messages provided'})
    return

  if not model:
    emit('error', {'error': 'No model provided'})
    return

  if isinstance(model, list):
    model = model[0]
  process_id = str(uuid.uuid4())
  table = statusTable("processes", app)
  table.create_status(process_id)
  emit('response', {'process_id': process_id})

  executor = Executor(app)
  try:
    executor.submit(get_response_from_openai, messages, process_id, table=table, model=model)
    print("Process submitted")
  except Exception as e:
    print(f"Error submitting process: {e}")
    emit('error', {'error': 'Error submitting process'})