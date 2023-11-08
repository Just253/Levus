from src.command import Botcommand
import pyautogui
# libraries = pyautogui, os, re
class Command(Botcommand):
  name = 'escribe'
  description = 'Escribe un texto'	
  needArgument = True
  def execute(self, *args):
    pyautogui.typewrite(args[0])