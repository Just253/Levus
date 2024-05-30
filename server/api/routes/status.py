from flask import Flask, request, jsonify

app = Flask(__name__)

process_status = {}

@app.route('/status/<process_id>', methods=['GET'])
def get_status(process_id):
    status = process_status.get(process_id)
    if status:
        return jsonify(status)
    else:
        return jsonify({"error": "Process ID not found"}), 404

def update_process_status(process_id, status, response=None, error=None):
    process_status[process_id] = {
        "status": status,
        "response": response,
        "error": error
    }

if __name__ == '__main__':
    app.run()
