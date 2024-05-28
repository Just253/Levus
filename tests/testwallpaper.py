import ctypes

class ChangeWallpaper:
    def __init__(self, wallpaper_path):
        self.wallpaper_path = wallpaper_path

    def change(self):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.wallpaper_path, 3)

if __name__ == "__main__":
    wallpaper_path = input("Please enter the path to the wallpaper image: ")
    changer = ChangeWallpaper(wallpaper_path)
    changer.change()