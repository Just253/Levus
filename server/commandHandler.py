import inspect
import importlib, os
class CommandHandler:
  def __init__(self, commands_Path):
    self.commands_Path = commands_Path
    self.commands = []

  def get_method_info(self,method):
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
  def get_class_info(self,cls):
    parameters, required = self.get_method_info(cls.execute)
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
  
  def get_info_from_name(self,name):
    command_module = importlib.import_module(f"commands.{name}")
    command_module = getattr(command_module, "BotCommand")
    return self.get_class_info(command_module)
  
  def getFiles(self):
    command_files = os.listdir(self.commands_Path.replace('.',  os.sep))
    command_files = [file[:-3] for file in command_files if file.endswith(".py")]
    return command_files
  
  def make_tools(self):
    for command_file in self.getFiles():
       self.add_tool(command_file)
    return self.commands
  def add_tool(self, name_file):
    index, tool = self.search_tool(name_file)
    new_tool = {
         "type": "function",
         "function": self.get_info_from_name(name_file)
      }
    if tool:
        self.commands[index] = new_tool
    else:
        self.commands.append(new_tool)
    return True
  def remove_tool(self, name):
    index, tool = self.search_tool(name)
    if tool:
        self.commands.pop(index)
        return True
    return False
  
  def search_tool(self, name):
    for i, command in enumerate(self.commands):
        if command["function"]["name"] == name:
            return i, command
    return None, None
  def get_tools(self):
    return self.commands  
      
#class_info = get_class_info(BotCommand)
#json_info = json.dumps(class_info, indent=4)

#print(json_info)