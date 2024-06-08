from flask import Flask, Blueprint
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import importlib
from .api.functions.commandHandler import CommandHandlerObserver

load_dotenv()
socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    # Importar automáticamente todas las clases de los directorios de api/routes/
    routes_dir = os.path.join(os.path.dirname(__file__), 'api', 'routes')
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                module = importlib.import_module(f'server.api.routes.{filename[:-3]}')
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, Blueprint):
                        app.register_blueprint(attr)
            except Exception as e:
                print(f"Error al importar el módulo {filename}: {e}")

    observer = CommandHandlerObserver(os.path.join(os.path.dirname(__file__), 'commands'), app)
    observer.commandHandler.logging = True

    from . import connections
    socketio.init_app(app)
    return app
    