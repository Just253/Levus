from src.command import Botcommand

class Command(Botcommand):
    name = 'silencio'
    description = 'Silencia la voz de la IA'
    needArgument = False

    def execute(self, *args):
        self.BOT._IA.set_silent(True)  