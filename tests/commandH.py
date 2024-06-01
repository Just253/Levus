import inspect
def get_method_info(method):
    docstring = inspect.getdoc(method)
    lines = docstring.split("\n")

    parameters = {}
    required = []
    sig = inspect.signature(method)
    for param in sig.parameters.values():
        if param.default == inspect.Parameter.empty and param.name != 'self':
            required.append(param.name)

    for line in lines:
        if ":param" in line:
            _, param_info = line.split(":param")
            param_name, param_desc = param_info.split(":")
            param_name = param_name.strip()
            param_type = "string" if "url" in param_name else "boolean"
            parameters[param_name] = {"type": param_type, "description": param_desc.strip()}

    return parameters, required

def get_class_info(cls):
    parameters, required = get_method_info(cls.execute)
    class_info = {
        "name": cls.name,
        "description": cls.description,
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": required,
        },
    }
    return class_info

import importlib, os 
commands_Path = "server.commands"
command_files = os.listdir(commands_Path.replace('.',  os.sep))
command_files = [file[:-3] for file in command_files if file.endswith(".py")]
print(command_files)
commands = []
for command_file in command_files:
    command_module = importlib.import_module(f"commands.open_url")
    command_module = getattr(command_module, "BotCommand")
    print(get_class_info(command_module))
