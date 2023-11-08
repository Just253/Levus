
from src.command import Botcommand
import requests
import pyttsx3
# libraries: requests, pyttsx3

class Command(Botcommand):
  name = 'decirme'
  description = 'Busca en Google y dice los resultados con tts'
  needArgument = True

  def execute(self, *args):
    # Buscar en Google el argumento
    query = args[0]
    url = f'https://www.google.com/search?q={query}'
    response = requests.get(url)
    # Extraer los títulos y snippets de los resultados
    results = response.text.split('<div class="g">')
    titles = []
    snippets = []
    for result in results[1:]:
      title = result.split('<h3 class="LC20lb DKV0Md">')[1].split('</h3>')[0]
      snippet = result.split('<span class="aCOpRe"><span class="f">')[1].split('</span></span>')[0]
      titles.append(title)
      snippets.append(snippet)
    # Inicializar el motor de tts
    engine = pyttsx3.init()
    # Decir el número de resultados encontrados
    engine.say(f'Se han encontrado {len(titles)} resultados para {query}')
    engine.runAndWait()
    # Decir cada título y snippet
    for i in range(len(titles)):
      engine.say(f'Resultado número {i+1}: {titles[i]}')
      engine.say(snippets[i])
      engine.runAndWait()
