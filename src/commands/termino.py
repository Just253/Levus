from src.command import Botcommand
class Command(Botcommand):
  name = 'detente'
  description = 'Termina el proceso'
  def execute(self,*args):
    self.BOT.stopAll()
    print('Termino')