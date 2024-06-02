from flask import jsonify, Blueprint
from flask import current_app as app
from ..functions.db import get_status as get_status_fn

status_bp = Blueprint('status', __name__)


@status_bp.route('/status/<process_id>', methods=['GET'])
def get_status(process_id):
    status = get_status_fn(process_id, "processes", app)
    if status.get('error'):
        return jsonify(status), 404
    return jsonify(status)