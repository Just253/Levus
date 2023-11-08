from src.command import Botcommand
import win32gui

class Command(Botcommand):
  name = 'ocultar ventanas'
  description = 'Oculta todas las ventanas abiertas en el escritorio'
  needArgument = False
  def execute(self, *args):
    # Obtener el identificador de la ventana del escritorio
    desktop = win32gui.GetDesktopWindow()
    # Obtener una lista de todas las ventanas abiertas
    windows = []
    win32gui.EnumWindows(lambda hwnd, windows: windows.append(hwnd), windows)
    # Ocultar cada ventana que no sea el escritorio
    for window in windows:
      if window != desktop:
        win32gui.ShowWindow(window, 0) # 0 es el código para ocultar
    print('Ventanas ocultadas')