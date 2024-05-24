from flask import Blueprint, request
#from api.functions import pass

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    # ...
    pass