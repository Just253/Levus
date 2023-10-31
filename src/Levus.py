from src.eventCommandHandler import CommandHandler
from src.bots.gtp4free import Botia
from src.voiceToText.annyangV2 import Annyang
from watchdog.observers import Observer
import os
#TODO: añadirle la funcion de reconocimiento de voz y gestos para ser administrados por la IA
class Levus():
  _bot_name = 'avestruz' # For now it is the name of the bot 
  _commands = []
  _debug = True
  _IA = Botia()
  def __init__(self):
    self.annyang = Annyang(self)
    self.annyang._debug = True

    command_dir = os.path.join(os.path.dirname(__file__), "commands")
    self.command_handler = CommandHandler(self, command_dir)
    self.observer = Observer()
    self.observer.schedule(self.command_handler, path=command_dir, recursive=True)
  async def start(self):
    self.observer.start()
    await self.annyang.start()

  def getBotName(self):
    pass
  def startVoiceRecognition(self):
    pass
  def stopVoiceRecognition(self):
    pass
  def startImageRecognition(self):
    pass
  def stopImageRecognition(self):
    pass
  def stopAll(self):
    pass
  def add_commands(self, commands):
    if self._debug: print("[DEBUG] add_commands - NEW COMMANDS - " + str(commands))
    for phrase, callback in commands.items():
      self._commands.append((phrase, callback))
  def remove_commands(self, commands):
    if isinstance(commands, str):
      commands = [commands]
        
    if self._debug: print("[DEBUG] remove_commands - OLD COMMANDS - " + str(self._commands))
    self._commands = [(phrase, callback) for phrase, callback in self._commands if phrase not in commands]
  
  def get_bot_name(self):
    return self._bot_name
  def set_bot_name(self, name):
    self._bot_name = name
  
  def check_commands(self, text):
    text_lower = text.lower()
    for phrase, callback in self._commands:
        if phrase.lower() in text_lower:
            if self._debug: print(f'Command matched: {phrase}')
            text = text[text_lower.index(phrase.lower()) + len(phrase):]
            try:
                command = callback(self)
                command.execute(text)
            except Exception as e:
                if self._debug:
                    print(f'Error executing {phrase}: {e}')
            return True
    return False
  def cleanText(self, command, text):
    pass
  async def askIA(self,text):
    response = await self._IA.askInternet(text)
    print(response)
    return response
    