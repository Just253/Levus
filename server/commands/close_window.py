from command import Command
class BotCommand(Command):
    name="close_window"
    description="este comando cierra una ventana"
    def execute(self, processName:str):
        """
        :param processname: npmbre del proceso a cerrar
        :type processname: string
        """
        # TODO: Implementar el cierre de la ventana mendiante nombre/ID del proceso
        # if is int -> kill by ID
        # if is str -> kill by name
        import os
        os.system(f"taskkill /f /im {processName}")
        

