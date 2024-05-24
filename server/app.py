from flask import Flask, Blueprint
import os
import importlib

app = Flask(__name__)

# Importar automáticamente todas las clases de los directorios de api/routes/
routes_dir = os.path.join(os.path.dirname(__file__), 'api', 'routes')
for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module = importlib.import_module(f'api.routes.{filename[:-3]}')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                app.register_blueprint(attr)

if __name__ == '__main__':
    app.run(debug=True)