from .command import Command
import ctypes

class BotCommand(Command):
    name="hide_all"
    description="este comando oculta todas las ventanas"
    
    def execute(self):
        # presionar tecla
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Tecla Windows abajo
        ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # Tecla D abajo
        # soltar tecla
        ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)  # Tecla D arriba
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Tecla Windows arriba