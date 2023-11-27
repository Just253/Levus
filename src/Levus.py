from src.eventCommandHandler import CommandHandler
from src.bots.gtp4free import Botia
from src.voiceToText.annyangV2 import Annyang
from src.gestureToTxt.main import HandGesture
from watchdog.observers import Observer

import os, asyncio, pyttsx3, re, threading, time
class Levus():
  bot_name = 'gato' # For now it is the name of the bot 
  _commands = []
  _commands_voice = []
  _commands_image = []
  _debug = True
  _IA = Botia()
  voiceRecognitionActive = False
  imageRecognitionActive = False
  observer = Observer()
  def __init__(self):
    self.annyang = Annyang(self)
    self.imageReconigtion = HandGesture(self)
    self.annyang._debug = True

    command_dir = os.path.join(os.path.dirname(__file__), "commands")
    self.command_handler = CommandHandler(self, command_dir)
    self.observer.schedule(self.command_handler, path=command_dir, recursive=True)
  def start(self):
    self.observer.start()

  def voiceRecognitionToggle(self):
    if self.voiceRecognitionActive:
      self.annyang.abort()
      self.voiceRecognitionActive = False
    else:
      threading.Thread(target=self.annyang.start).start()
      self.voiceRecognitionActive = True
    
  def imageRecognitionToggle(self):
    if self.imageRecognitionActive:
      print('imageRecognitionToggle - STOP')
      self.imageReconigtion.stop()
      self.imageRecognitionActive = False
    else:
      print('imageRecognitionToggle - START')
      threading.Thread(target=self.imageReconigtion.start).start()
      self.imageRecognitionActive = True
  def stopAll(self):
    if self.voiceRecognitionActive:
      self.annyang.abort()
    if self.imageRecognitionActive:
      self.annyang.abort()
  def add_commands(self, commands, support_gestor=False, support_voice=False):
    if self._debug: print("[DEBUG] add_commands - NEW COMMANDS - " + str(commands))
    for phrase, callback in commands.items():
      self._commands.append((phrase, callback))
      if support_voice:
        self._commands_voice.append((phrase, callback)) 
      if support_gestor:
        self._commands_image.append((phrase, callback))
  def remove_commands(self, commands):
    if isinstance(commands, str):
      commands = [commands]
        
    if self._debug: print("[DEBUG] remove_commands - OLD COMMANDS - " + str(self._commands))
    self._commands = [(phrase, callback) for phrase, callback in self._commands if phrase not in commands]
    self._commands_voice = [(phrase, callback) for phrase, callback in self._commands if phrase not in commands]
    self._commands_image = [(phrase, callback) for phrase, callback in self._commands if phrase not in commands]
  
  def get_bot_name(self):
    return self.bot_name
  def set_bot_name(self, name):
    self.bot_name = name
  
  def get_finger_positions(self):
    return self.imageReconigtion.getLastFingersPositions()

  def check_voice_commands(self, text):
    text_lower = text.lower()
    isCommand = False
    for phrase, callback in self._commands_voice:
        if phrase.lower() in text_lower:
            isCommand = True
            if self._debug: print(f'Command matched: {phrase}')
            text = text[text_lower.index(phrase.lower()) + len(phrase):]
            try:
                from src.command import Botcommand
                command: Botcommand = callback(self)
                if command.needArgument and text == '':
                  print('FALTA ARGUMENTO')  
                  break
                command.execute(text)
                break
            except Exception as e:
                if self._debug: print(f'Error executing {phrase}: {e}')
    if isCommand == False:
      asyncio.run(self.askIA(text))
  def check_gesture_commands(self, finger_positions):
    for phrase, callback in self._commands_image:
        from src.command import Botcommand
        command: Botcommand = callback(self)
        if command.activate(finger_positions):
          if command.running:
            break
          try:
            command.running = True
            command.execute()
            if command.needWait:
              time.sleep(command.timeWait)
            command.running = False
            break
          except Exception as e:
              if self._debug: print(f'Error executing {phrase}: {e}')
  async def askIA(self,text):
    response = await self._IA.askInternet(text, temperature=0.1)
    print(response)
    try: pyttsx3.speak(response)
    except Exception as e:
      if self._debug: print(e)
      
    return text