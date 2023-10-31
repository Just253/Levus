from src.Levus import Levus
class Botcommand:
  BOT: Levus
  needArgument = False
  def __init__(self,BOT: Levus):
    self.description = ''
    self.BOT = BOT

  def execute(self, *args):
    # ...
    print('')

  def help(self):
    # use tts 
    print(f'Usage: {self.name} [args]')
    print(self.description)
  def getCommandName(self):
    return self.name