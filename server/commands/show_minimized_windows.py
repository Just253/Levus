from .command import Command
from pywinauto import Desktop
import psutil

class BotCommand(Command):
  name = "show_minimized_windows"
  description = "Shows all windows if they are minimized"
  
  def execute(self):
    windows = Desktop(backend="win32").windows()
    blacklist = ["System", "svchost", "DWM Notification Window"]
    for win in windows:
      try:
        window_text = win.window_text()  # Obtener el texto de la ventana
        if win.is_minimized() and window_text:  # Verificar si la ventana está minimizada
          pid = win.process_id()  # Obtener el PID de la ventana
          process = psutil.Process(pid)  # Obtener el objeto de proceso usando psutil
          process_name = process.name()
          # Verificar contra la lista negra tanto el nombre del proceso como el texto de la ventana
          if not any(blacklisted_word in process_name or blacklisted_word in window_text for blacklisted_word in blacklist):
            print(f"Restaurando ventana: {window_text}")
            win.restore()  # Restaurar la ventana
      except Exception as e:
        print(f"Error al restaurar la ventana: {e}")