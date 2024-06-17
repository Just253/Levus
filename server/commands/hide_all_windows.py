from .command import Command
import pyautogui

class BotCommand(Command):
    name="hide_all_windows"
    description="este comando oculta todas las ventanas"
    
    def execute(self):
        # presionar tecla
        pyautogui.hotkey('win', 'd')