from command import Command
class BotCommand(Command):
    name="close_all"
    description="este comando cierra todas las tareas en proceso "
    def execute(self, processName):
        import os
        os.system('taskkill /F /FI "STATUS eq RUNNING"')
        

