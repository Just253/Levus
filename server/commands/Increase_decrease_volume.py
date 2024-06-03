import os
import ctypes
from command import Command
class BotCommand(Command):
    name="volume change"
    description="este comando modifica el volumen de la aplicacion que lo ejecuta"
    
    def execute(self,nuevo_volumen:int):
        """
        :param nuevo_volumen: volumen ingresado por el usuario
        :type nuevo_volumen: int
        """
        #self.obtener_volumen()
        self.cambiar_volumen(nuevo_volumen)

    def obtener_volumen(self):
        #declaro una constante que declara cual es el identificador de audio del dispositivo el audio
        #predeterminado suele ser 0 aunque este cambia depende si hay mas disposituvos de salida
        constante=0
        
        #declaro el nombre de la clase que llamo para no escribir tanta cosa
        #en este caso seria el dll de win multimedia (winmm) que es el que tiene acceso al audio
        winm= ctypes.windll.winmm
        
        #se crea un objeto que es el que va a almacenar el audio en este caso con un almacenador de 32 bits
        tamañoVolumen = ctypes.c_ulong()
        winm.waveOutGetVolume(constante, ctypes.byref(tamañoVolumen))
        
        # Convertir el valor del volumen de 32 bits a uno de 0 a 100
        volume = (tamañoVolumen.value & 0xFFFF) / 65535 * 100
        return volume
    def cambiar_volumen(self, nuevo_volumen):
        # Convertir el porcentaje de volumen a un valor entre 0 y 65535
        nuevo_volumen = int(nuevo_volumen / 100 * 65535)
        ctypes.windll.winmm.waveOutSetVolume(0, nuevo_volumen)