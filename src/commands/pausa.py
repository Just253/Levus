
from src.command import Botcommand
import pyautogui
# libraries: os
class Command(Botcommand):
  name = 'pausa música'
  alternatives = ['continua musica', 'musica play', 'pausa', 'play']
  description = 'Pausa la música que se esté reproduciendo'
  needArgument = False
  support_gestor = True
  def execute(self, *args):
    pyautogui.hotkey('playpause')
  def activate(self, finger_positions):
    return self.BOT.imageReconigtion.check_up_fingers(['index'])