from src.command import Botcommand
import pyautogui

class Command(Botcommand):
    name = 'diapositiva siguiente'
    alternatives = ['anterior diapositiva', 'siguiente diapositiva', 'diapositiva anterior']
    description = 'Realiza la acción de siguiente diapositiva'
    needArgument = False

    def execute(self, *args):
      text = args[0]
      phrase = args[1]
      if phrase == 'anterior diapositiva' or phrase == 'diapositiva anterior':
        pyautogui.press('left')
      
      if phrase == 'diapositiva siguiente' or phrase == 'siguiente diapositiva':
        pyautogui.press('right')
