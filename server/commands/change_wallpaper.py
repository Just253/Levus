from os import path
from ctypes import windll
from .command import Command

class BotCommand(Command):
    name = "change_wallpaper"
    description = "Changes the wallpaper"
    def execute(self, directory: str, image_name: str):
        """
        :param directory: La ruta del directorio donde se encuentra la imagen
        :type directory: string
        :param image_name: El nombre de la imagen + su extensión de formato
        :type image_name: string
        """
        wallpaper_path = path.join(directory, image_name)
        if path.exists(wallpaper_path):
            SPI_SETDESKWALLPAPER = 20
            windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)
        else:
            print(f"No se encontró la imagen {image_name} en el directorio {directory}")