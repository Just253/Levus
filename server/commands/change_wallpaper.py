import os
import ctypes
from command import Command

class ChangeWallpaperCommand(Command):
    name = "change_wallpaper"
    description = "Changes the wallpaper"
    def execute(self, directory, image_name):
        wallpaper_path = os.path.join(directory, image_name)
        if os.path.exists(wallpaper_path):
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)
        else:
            print(f"No se encontró la imagen {image_name} en el directorio {directory}")