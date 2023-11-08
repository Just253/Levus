from src.command import Botcommand
import asyncio

class Command(Botcommand):
  name = 'crea un comando'
  description = 'Crea un nuevo comando'
  needArgument = True

  def execute(self, *args):
    asyncio.create_task(self.BOT._IA.newCommand(args[0]))