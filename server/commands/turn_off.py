import os
from command import Command
class BotCommand(Command):
    name="turn_off"
    description="este comando apaga la PC del usuario"
    def execute(self):
       
        'force shutdown with OS',os.system('shutdown /s')
        

