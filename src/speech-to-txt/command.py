from annyangV2 import Annyang
class Botcommand:
  BOT: Annyang
  def __init__(self,BOT):
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