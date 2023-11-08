from src.command import Botcommand
import os
class Command(Botcommand):
  name = 'menciona'
  description = 'Dice el nombre de un comando'
  needArgument = True
  def execute(self,*args):
    comando = args[0].strip()
    for command in self.BOT._commands:
        fileName = os.path.basename(command[1].filePath)[:-3]
        if fileName == comando:
            return print(f"El nombre del comando {comando} es {command[1].getCommandName(command[1])}")
    print(f'Comando {comando} no encontrado')