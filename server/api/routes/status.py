from flask import jsonify, request, Blueprint
from flask import current_app as app
from ...tinydb_flask import TinyDB as TDB
from tinydb import TinyDB, Query

db: TinyDB = TDB(app).get_db()

status_bp = Blueprint('status', __name__)

@status_bp.route('/status/<process_id>', methods=['GET'])
def get_status(process_id):
    process = db.Query()
    status = db.search(process.process_id == process_id)
    if status:
        status = status[0]  # Get the first (and likely only) status
        if status['status'] == 'completed':
            return jsonify({
                "state": status['status'],
                "process_id": status['process_id'],
                "response": status.get('response', '')
            })
        elif status['status'] == 'pending':
            return jsonify({
                "state": status['status'],
                "process_id": status['process_id'],
                "preview": status.get('preview', '')
            })
        elif status['status'] == 'error':
            return jsonify({
                "state": status['status'],
                "process_id": status['process_id'],
                "preview": status.get('preview', ''),
                "error": status.get('error', '')
            })
    else:
        return jsonify({"error": "Process ID not found"}), 404

def create_status(process_id):
    db.insert({"process_id": process_id, "status": "pending", "preview": "", "response": "", "error": ""})

def update_status( process_id, **kwargs):
    query = Query()
    process = db.search(query.process_id == process_id)
    if process:
        db.update(**kwargs, query.process_id == process_id)
        return 200