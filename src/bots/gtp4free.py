import g4f, asyncio
g4f.debug.logging = True
from g4f.Provider import (GeekGpt, Bing, You)
from typing import List, Union


# TODO: Separar el tipo de bots a usar, tanto para responder preguntas basicas, y de ahi administrarlo para tener contactor con internet y programar
class Botia():
  _IA_programming = []
  _IA_chat = []
  _IA_internet = []
  # _messages = []

  def __init__(self) -> None:
    pass
  async def _send_messages(self, Provider: object = None, model: Union[object, str] = 'gpt-3.5-turbo', text: str = '', messages: List[dict] = None):
    if text == '' or text is None:
      return "[Error] No text"
    if messages is None:
      messages = [{"role": "user", "content": text}]
    try: 
      response = await g4f.ChatCompletion.create_async(
        provider=Provider,
        model=model,
        messages= messages,
        stream=False,
        ignored=["Phind", "NooAi", "You", "GptForLove", "ChatBase"]
      )
      return response
    except Exception as e:
      return e

  async def ask(self,text):
    models = g4f.models.gpt_35_turbo
    response = await self._send_messages(model=models, text=text)
    return response
  async def askProgramming(self, text):
    provider = GeekGpt
    response = await self._send_messages(Provider=provider, text=text)
    return response
  async def askInternet(self,text):
    provider = Bing
    response = await self._send_messages(Provider=provider, text=text)
    return response
  async def newCommand(self,text):
    messages = [{"role": "system", "content": "Eres una IA que busca resolver problemas cotidianos al usar una PC, simula que tienes el control total de la computadora para que el usuario pueda trabajar sin manos | Una Api de referencia | from annyangV2 import Annyang\nclass Botcommand:\n  BOT: Annyang\n  needArgument = False\n  def __init__(self,BOT):\n    self.description = ''\n    self.BOT = BOT\n\n  def execute(self, *args):\n    # ...\n    print('')\n\n  def help(self):\n    # use tts \n    print(f'Usage: {self.name} [args]')\n    print(self.description)\n  def getCommandName(self):\n    return self.name | ese es el cuerpo de la API, ahora un ejemplo de uso | from src.command import Botcommand\n\nclass Command(Botcommand):\n name = 'cambiar nombre'\n description = 'Cambia el nombre del bot'\n needArgument = True\n def execute(self, *args):\n if args[0] is None:\n return print('Especifica un nombre')\n newName = args[0].strip().lower()\n self.BOT.set_bot_name(newName)\n print(f'Nombre cambiado a {newName}|')\n print(self.BOT.get_bot_name())\n | No respondas nada , ni guies, tienes que seguir las mismas caracteristicas, todo el codigo va dentro del execute, no fuera" }, {"role": "user", "content": text}]

    provider = GeekGpt
    response = await self._send_messages(Provider=provider,text=text, messages=messages)
    return response
"""  
async def main():
  botManager = Botia()
  while True:
    txt = input(">> ")
    response = await botManager.newCommand(txt)
    print(response)

asyncio.run(main())
"""