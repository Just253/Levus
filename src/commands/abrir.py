
from src.command import Botcommand
import webbrowser
# libraries = webbrowser
class Command(Botcommand):
  name = 'abrir'
  description = 'Abre una página web con solo decir su nombre'
  needArgument = True
  def execute(self, *args):
    # Se asume que el argumento es el nombre de la página web, sin el dominio
    # Por ejemplo, si el argumento es 'bing', se abre 'https://www.bing.com'
    # Se usa una lista de dominios comunes para intentar encontrar la página web
    # Si no se encuentra, se muestra un mensaje de error
    name = args[0].lower()
    domains = ['.com', '.es', '.org', '.net', '.edu', '.gov']
    for domain in domains:
      url = 'https://' + name + domain
      try:
        webbrowser.open(url)
        return
      except:
        pass
    print(f'No se pudo abrir la página web {name}')
