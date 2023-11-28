
from src.command import Botcommand
import pyautogui
# libraries: os
class Command(Botcommand):
  name = 'pausa música'
  alternative = ['continua musica', 'musica play', 'pausa', 'play']
  description = 'Pausa la música que se esté reproduciendo'
  needArgument = False
  def execute(self, *args):
    pyautogui.hotkey('playpause')
