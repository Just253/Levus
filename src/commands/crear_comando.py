from src.command import Botcommand
import asyncio

class Command(Botcommand):
  name = 'crea un comando'
  description = 'Crea un nuevo comando'
  needArgument = True

  def execute(self, *args):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(self.BOT._IA.newCommand(args[0]))