from src.command import Botcommand
import pyautogui

class Command(Botcommand):
  name = 'ocultar ventanas'
  description = 'Oculta todas las ventanas abiertas en el escritorio'
  needArgument = False
  def execute(self, *args):
    pyautogui.hotkey('win', 'd')