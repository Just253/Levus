import os
import subprocess
from command import Command

class BotCommand(Command):
    name = "run_exe"
    description = "Runs a specified .exe file"
    def execute(self, directory, program_name):
        exe_path = os.path.join(directory, program_name)
        if os.path.exists(exe_path):
            subprocess.run(exe_path, shell=True)
        else:
            print(f"No se encontró el programa {program_name} en el directorio {directory}")