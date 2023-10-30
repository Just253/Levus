from command import Botcommand

class Command(Botcommand):
  name = 'cambiar nombre'
  description = 'Cambia el nombre del bot|'
  def execute(self, *args):
    if args[0] is None:
      return print('Especifica un nombre')
    newName = args[0].strip().lower()
    self.BOT.set_bot_name(newName)
    print(f'Nombre cambiado a {newName}|')
    print(self.BOT.get_bot_name())
