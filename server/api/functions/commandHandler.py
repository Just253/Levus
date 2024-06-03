import inspect
import importlib, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from . import TDB
from tinydb import Query
from tinydb.table import Table
import sys
class dbCommands:
  query = Query()
  def __init__(self, app):
    self.db: Table = TDB(app).get_db().table("commands")
  def exists(self,commandName):
    return len(self.db.search(self.query.name == commandName)) > 0
  def addCommand(self,commandName,commandInfo):
    if self.exists(commandName):
      return False
    self.db.insert({"name": commandName, "info": commandInfo})
  def updateCommand(self,commandName,commandInfo):
    self.db.update({"info": commandInfo}, self.query.name == commandName)
  def removeCommand(self,commandName):
    self.db.remove(self.query.name == commandName)
  def getCommand(self, commandName):
    result = self.db.search(self.query.name == commandName)
    return result[0] if result else None
  def getTool(self,commandName):
    return self.getCommand(commandName)["info"]
  def getCommands(self):
    return self.db.all()
  def getTools(self):
    return [command["info"] for command in self.getCommands()]
  def getToolsNames(self):
    return [command["name"] for command in self.getCommands()]
  def getModuleFromName(self,commandName):
    return importlib.import_module(f"server.commands.{commandName}")
  def getCommandClass(self,commandName):
    return getattr(self.getModuleFromName(commandName), "BotCommand")
  def get_tools_info(self, tools):
    tools_info = []
    for tool in tools:
        tool_info = self.getTool(tool)
        tools_info.append(tool_info)
    return tools_info
      
class CommandHandler:
  logging = False
  def __init__(self, commands_Path,app):
    self.commands_Path = commands_Path
    self.commands = []
    self.db = dbCommands(app)
    self.make_tools()

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
          param_desc = param_desc.strip()
          parameters[param_name] = {"description": param_desc}
      elif ":type" in line:
          _, type_info = line.split(":type")
          type_name, type_desc = type_info.split(":")
          type_name = type_name.strip()
          type_desc = type_desc.strip()
          if type_name in parameters:
              parameters[type_name]["type"] = type_desc
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
    return [file[:-3] for file in os.listdir(self.commands_Path.replace('.', os.sep)) if file.endswith(".py")]
  
  def make_tools(self):
    for command_file in self.getFiles():
       self.add_tool(command_file)
    return self.commands
  def add_tool(self, name_file):
    try:
      new_tool = {
          "type": "function",
          "function": self.get_info_from_name(name_file)
        }
      if self.db.exists(name_file):
        self.db.updateCommand(name_file,new_tool)
      else:
        self.db.addCommand(name_file,new_tool)
    except Exception as e:
      if self.logging:
        print(f"Error al agregar la herramienta {name_file}: {e}")
  def remove_tool(self, name):
    self.db.removeCommand(name)
      

class CommandHandlerObserver(FileSystemEventHandler):
  def __init__(self, file_path, app):
    self.commandHandler = CommandHandler(file_path, app)
    self.observer = Observer()
    self.observer.schedule(self, self.commandHandler.commands_Path, recursive=True)
    self.observer.start()

  def getFileName(self, event):
    filename = event.src_path.split(os.sep)[-1]
    isPy = filename.endswith(".py")
    return filename[:-3], isPy

  def handle_event(self, event, action):
    filename, isPy = self.getFileName(event)
    if isPy:
      action(filename)

  def on_modified(self, event):
    self.handle_event(event, self.commandHandler.add_tool)

  def on_created(self, event):
    self.handle_event(event, self.commandHandler.add_tool)

  def on_deleted(self, event):
    self.handle_event(event, self.commandHandler.remove_tool)

  def on_moved(self, event):
    def action(filename):
      self.commandHandler.remove_tool(filename)
      self.commandHandler.add_tool(filename)
    self.handle_event(event, action)

  def stop(self):
    self.observer.stop()
    self.observer.join()