from flask import Flask, Blueprint
from dotenv import load_dotenv
import os
import importlib
from tinydb_flask import TinyDB

load_dotenv()
app = Flask(__name__)
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
db = TinyDB(app).get_db()

# Importar automáticamente todas las clases de los directorios de api/routes/

routes_dir = os.path.join(os.path.dirname(__file__), 'api', 'routes')
for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        try:
            module = importlib.import_module(f'api.routes.{filename[:-3]}')
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
        except Exception as e:
            print(f"Error al importar el módulo {filename}: {e}")
            
if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, port=5000)