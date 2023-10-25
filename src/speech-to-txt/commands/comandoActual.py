from command import Botcommand
from annyangV2 import Annyang
class Command(Botcommand):
  name='dime todos los comandos'
  description='Muestra todos los comandos'
  def execute(self,*args):
    for command in self.BOT._commands:
      print(f"El nombre del comando {command[1].getCommandName(command[1])}")
    print(f'Listo')