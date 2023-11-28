import g4f, asyncio, logging, re, io, subprocess
g4f.debug.logging = True
from g4f.Provider import (GeekGpt, Bing, You)
from typing import List, Union
import os.path
logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)

def get_python_command():
    """Devuelve el comando para ejecutar Python en este sistema."""
    try:
        subprocess.check_output(["python", "--version"])
        return "python"
    except Exception:
        try:
            subprocess.check_output(["py", "--version"])
            return "py"
        except Exception:
            raise EnvironmentError("Python no está disponible en el PATH del sistema")

async def verifica_instala_libreria(library_name):
    """Verifica si una biblioteca está instalada, y si no, la instala."""
    python_command = get_python_command()
    try:
        __import__(library_name)
        logging.info(f"The library {library_name} is already installed.")
        return True
    except ImportError:
        logging.info(f"The library {library_name} is not installed. Installing...")
        process = await asyncio.create_subprocess_exec(
            python_command, "-m", "pip", "install", library_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            logging.info(f"The library {library_name} has been installed successfully.")
            return True
        else:
            logging.error(f"Error installing {library_name}: {stderr.decode()}")
            return False

def limpiar_texto(texto):
    # Eliminar enlaces
    texto = re.sub(r'http\S+|www.\S+', '', texto, flags=re.MULTILINE)
    # Eliminar citas
    texto = re.sub(r'\[\^\d+\^\]\[\d+\]', '', texto, flags=re.MULTILINE)
    # Eliminar referencias de enlaces
    texto = re.sub(r'\[\d+\]:', '', texto, flags=re.MULTILINE)
    return texto

class Botia():
  _IA_programming = Bing # Bing tiene GPT4 por que le da bien programar comandos cortos
  _IA_chat = Bing 
  _IA_internet = Bing
  _messages_internet = [{"role": "System", "content": "TU FUNCION ES RESUMIRLE NOTICIAS DEL INTERNET CUANDO TE LO PIDA, DEBES SER PRECISO Y DIRECTO, NO DIGAS MAS DE LO QUE EL USUARIO TE DIGA O SEA NECESARIO, NO ALARGUES LAS RESPUESTAS, NO TE DAN PUNTOS SI LO HACES. Eres una IA para ayudar a los usuarios en las tareas de resumir o explicar noticias del Internet. QUE TUS RESPUESTAS POR PREDETERMINADO SEAN MAXIMO 2 ORACIONES AH NO SER QUE EL USUARIO DIGA EXPLICITAMENTE QUE SE AUMENTE, TU USAS UNICAMENTE PYTHON "}]

  def __init__(self) -> None:
    pass
  async def _send_messages(self, Provider: object = None, model: Union[object, str] = 'gpt-3.5-turbo', text: str = '', messages: List[dict] = None, temperature = 0.1, **kwargs):
    if not text:
      return "[Error] No text"
    
    if messages is None:
      messages = [{"role": "user", "content": text}]
    
    try: 
      response = await g4f.ChatCompletion.create_async(
        provider=Provider,
        model=model,
        messages= messages,
        stream=False,
        ignored=["Phind", "NooAi", "You", "GptForLove", "ChatBase"],
        temperature=temperature
      )

      return response
    except Exception as e:
      logging.error(e)
      return await self._send_messages(Provider=Provider, model=model, text=text, messages=messages, temperature=temperature, **kwargs)

  async def ask(self,text,temperature=0.2, **kwargs):
    models = g4f.models.gpt_35_turbo
    return await self._send_messages(model=models, text=text, temperature=temperature, **kwargs)
  
  async def askProgramming(self, text, **kwargs):
    model = g4f.models.gpt_4
    return await self._send_messages(Provider=self._IA_programming, text=text,model=model, **kwargs)
  
  async def askInternet(self,text,temperature=0.2, **kwargs):
    self._messages_internet.append({"role": "user", "content": text})
    response = await self._send_messages(Provider=self._IA_internet, text=text, temperature=temperature, messages=self._messages_internet, **kwargs)
    self._messages_internet.append({"role": "assistant", "content": response})
    return limpiar_texto(response)
  async def newCommand(self, text, **kwargs):
    dirname = os.path.dirname(__file__)
    command_class_path = os.path.join(dirname, os.pardir, "command.py")
    example_command_path = os.path.join(dirname, os.pardir, "commands", "escribe.py")

    with open(command_class_path, mode="r") as file:
        command_class_content = file.read()

    with open(example_command_path, mode="r") as file:
        example_command_content = file.read()

    prompt_start = "TU FUNCION ES CREAR CODIGO EN PYTHON PARA LO QUE PIDA EL USUARIO TENGAS O NO TENGAS ACCESO. Eres una IA que utiliza Python para ayudar a los usuarios a interactuar con su PC sin usar las manos. Aquí tienes una API de referencia: "
    prompt_middle = "Este es el cuerpo de la API. A continuación, un ejemplo de uso (siempre debe ir from src.command import Botcommand): "
    prompt_end = "Tus respuestas deben estar siempre en bloques de código. Solo proporciona el código que iría dentro del archivo. Sin comentarios dentro ni fuera del codigo, ni explicaciones. No cambies el nombre de la clase Command(). Si no puedes realizar una tarea, busca una solución alternativa. No uses archivos externos (.png, .jpg, etc.), solo librerías y/o archivos Python proporcionados en el ejemplo. Si usas una libreria escribe 'libraries: ...' separado por comas tambien su 'import ...'"

    prompt = prompt_start + command_class_content + prompt_middle + example_command_content + prompt_end

    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": text}]

    try:
      response = await self._send_messages(Provider=self._IA_programming, text=text, messages=messages, temperature=0.1, **kwargs)
    except Exception as e:
      logging.error(e)
      return await self.newCommand(text)
    logging.debug(f"[DEBUG - RESPONSE] {response}")
    
    script_content = re.sub(r'```python|```', '', response)
    name_match = re.search(r"name = '(.*)'", script_content)
    libraries_match = re.search(r"libraries: (.*)", script_content)

    if not name_match:
      return await self.newCommand(text)
    if libraries_match:
      libraries = libraries_match.group(1).split(",")
      for library in libraries:
          await verifica_instala_libreria(library.strip())
    name = name_match.group(1).replace(" ", "_")
    os.makedirs("src/commands", exist_ok=True)
    with io.open(f'src/commands/{name}.py', 'w', encoding='utf8') as f:
        f.write(script_content)
    return name