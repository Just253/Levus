
from src.command import Botcommand
import os
# libraries = webbrowser
class Command(Botcommand):
  name = 'abre'
  description = 'Abre aplicacion segun el nombre pasado como parametro'
  needArgument = True
  def execute(self, *args):
    if len(args) < 1:
      self.BOT.bot_speak("Respuesta invalida: Abrir que?")
      return

    app = str(args[0])
    app = app.replace(' ', '-')
    if os.name == 'nt': 
      os.system(f'start {app}')
