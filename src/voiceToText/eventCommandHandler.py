from watchdog.events import FileSystemEventHandler
import os, importlib.util
from annyangV2 import Annyang

class Handler(FileSystemEventHandler):
  _function_on_modified = ()
  _function_on_created = ()
  _function_on_deleted = ()
  _function_on_moved = ()
  def on_modified(self, event):
    print('File modified event', event.src_path)
    if self._function_on_modified:
      self._function_on_modified(event)
  def on_created(self, event):
    print('File created event', event.src_path)
    if self._function_on_created:
      self._function_on_created(event)
  def on_deleted(self, event):
    print('File deleted event', event.src_path)
    if self._function_on_deleted:
      self._function_on_deleted(event)
  def on_moved(self, event):
    print('File moved event', event.src_path)
    if self._function_on_moved:
      self._function_on_moved(event)
  
class CommandHandler(Handler):
  BOT:Annyang
  def __init__(self,BOT, comando_dir):
    self.BOT = BOT
    self.comando_dir = comando_dir
    self._addCommandsFromDirs(comando_dir)
      
  def _addCommandsFromDirs(self, path):
    comando_files = os.listdir(path)
    for filename in comando_files:
      filePath = os.path.join(path, filename)
      if os.path.isfile(filePath):
        self._add_command(filePath)
      else:
        self._addCommandsFromDirs(filePath)

  def _isValidFile(self, src_path):
    if not os.path.isfile(src_path): return False
    if self.comando_dir not in src_path: return False
    if not src_path.endswith('.py'): return False
    return src_path
    
  def _function_on_modified(self, event):
    self._remove_command(event.src_path)
    self._add_command(event.src_path)
  
  def _function_on_created(self, event):
    self._add_command(event.src_path)
  
  def _function_on_deleted(self, event):
    self._remove_command(event.src_path)
  
  def _function_on_moved(self, event):
    self._remove_command(event.src_path)
    self._add_command(event.src_path)

  def _fileNameToModule(self,filePath):
      module_name = filePath[:-3]
      module_path = os.path.join(self.comando_dir, filePath)
      spec = importlib.util.spec_from_file_location(module_name, module_path)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
      module.Command.filePath = filePath
      return module

  def _search_filename(self,filePath):
      for command in self.BOT._commands:
          if command[1].filePath == filePath:
              return command[1]
      return None
  
  def _add_command(self,filePath):
    try:
      filePath = self._isValidFile(filePath)
      if not filePath: return
      module = self._fileNameToModule(filePath)
      commandName = module.Command.getCommandName(module.Command)
      self.BOT.add_commands({commandName: module.Command})
    except Exception as e:
      print(f"[ERROR - _add_command] {e}")
  
  def _remove_command(self,filePath):
    try:
      filePath = self._isValidFile(filePath)
      if not filePath: return
      for command in self.BOT._commands:
          if command[1].filePath == filePath:
              self.BOT.remove_commands(command[0])
              break
    except Exception as e:
      print(f"[ERROR - _remove_command] {e}")
      