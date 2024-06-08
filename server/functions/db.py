from flask import Flask
from . import TDB
from tinydb import TinyDB, Query
from tinydb.table import Table

def get_table(name: str, app: Flask) -> Table:
    db: TinyDB = TDB(app).get_db()
    return db.table(name)

def get_status(process_id: int, name: str, app: Flask):
    db = get_table(name, app)
    process = Query()
    status = db.search(process.process_id == process_id)
    if status:
        status = status[0]  # Get the first (and likely only) status
        if status['status'] == 'completed':
            return {
                "status": status['status'],
                "process_id": status['process_id'],
                "response": status.get('response', '')
            }
        elif status['status'] == 'pending':
            return {
                "status": status['status'],
                "process_id": status['process_id'],
                "preview": status.get('preview', '')
            }
        elif status['status'] == 'error':
            return {
                "status": status['status'],
                "process_id": status['process_id'],
                "preview": status.get('preview', ''),
                "error": status.get('error', '')
            }
    else:
        return {"error": "Process ID not found"}

class statusTable:
    table: Table
    query = Query()
    def __init__(self, name: str, app: Flask):
        self.table = get_table(name, app)
    def get_table(self):
        return self.table
    def create_status(self, process_id: int):
        self.table.insert({"process_id": process_id, "status": "pending", "preview": "", "response": "", "error": ""})
    def update_status(self, process_id: int, **kwargs):
        process = self.table.search(self.query.process_id == process_id)
        if process:
            self.table.update(kwargs, self.query.process_id == process_id)