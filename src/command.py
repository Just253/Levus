from src.Levus import Levus
class Botcommand:
  BOT: Levus
  needArgument = False
  support_gestor = False
  support_voice = True
  estado = False
  name = ''
  description = ''
  running = False
  needWait = True
  timeWait = 1
  
  def __init__(self,BOT: Levus):
    self.BOT = BOT

  def execute(self, *args):
    pass
  def activate(self, finger_positions):
    pass
  def help(self):
    # TODO: posiblemente usar tts 
    print(f'Usage: {self.name} [args]')
    print(self.description)
  def getCommandName(self):
    return self.name
  def getCommandDescription(self):
    return self.description
  