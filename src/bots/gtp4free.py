import g4f
from g4f.Provider import Bing
g4f.debug.logging = True
response = g4f.ChatCompletion.create(
  model=g4f.models.gpt_35_long,
  messages=[
    {"role": "user", "content": "¿Que dia es hoy? y dame un codigo en python que realize reconocimiento de gestos con camara para cuando una persona haga un puño en la consola se escriba 'puño'"}
  ],
  stream=False
)

print(response)

# TODO: Separar el tipo de bots a usar, tanto para responder preguntas basicas, y de ahi administrarlo para tener contactor con internet y programar
class Botia():
  _IA_programming = []
  _IA_chat = []
  _IA_internet = []

  def __init__(self) -> None:
    pass
  async def ask(self):
    pass
  async def askProgramming(self):
    pass
  async def askInternet(self):
    pass
  async def newCommand(self):
    pass
  
