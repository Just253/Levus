from flask import jsonify, request, Blueprint
from flask import current_app as app
from ..functions import TDB
from tinydb import TinyDB, Query

status_bp = Blueprint('status', __name__)

def get_db():
    db: TinyDB = TDB(app).get_db()
    return db

@status_bp.route('/status/<process_id>', methods=['GET'])
def get_status(process_id):
    db = get_db()
    process = Query()
    status = db.search(process.process_id == process_id)
    if status:
        status = status[0]  # Get the first (and likely only) status
        if status['status'] == 'completed':
            return jsonify({
                "status": status['status'],
                "process_id": status['process_id'],
                "response": status.get('response', '')
            })
        elif status['status'] == 'pending':
            return jsonify({
                "status": status['status'],
                "process_id": status['process_id'],
                "preview": status.get('preview', '')
            })
        elif status['status'] == 'error':
            return jsonify({
                "status": status['status'],
                "process_id": status['process_id'],
                "preview": status.get('preview', ''),
                "error": status.get('error', '')
            })
    else:
        return jsonify({"error": "Process ID not found"}), 404

def create_status(process_id: int):
    db = get_db()
    db.insert({"process_id": process_id, "status": "pending", "preview": "", "response": "", "error": ""})

def update_status(process_id: int, **kwargs):
    db = get_db()
    query = Query()
    process = db.search(query.process_id == process_id)
    if process:
        db.update(kwargs, query.process_id == process_id)