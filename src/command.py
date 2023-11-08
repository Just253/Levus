from src.Levus import Levus
class Botcommand:
  BOT: Levus
  needArgument = False
  def __init__(self,BOT: Levus):
    self.name = ''
    self.description = ''
    self.BOT = BOT

  def execute(self, *args):
    pass

  def help(self):
    # TODO: posiblemente usar tts 
    print(f'Usage: {self.name} [args]')
    print(self.description)
  def getCommandName(self):
    return self.name
  def getCommandDescription(self):
    return self.description