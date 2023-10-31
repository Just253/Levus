from src.command import Botcommand
class Command(Botcommand):
  name = 'dime tu nombre'
  description = 'Muestra el nombre de bot'
  def execute(self, *args):
    print(f'Mi nombre es {self.BOT.get_bot_name()}')