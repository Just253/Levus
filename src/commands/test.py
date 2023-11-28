from src.command import Botcommand

class Command(Botcommand):
    name = 'test'  # Nombre del comando para usarlo en la linea de comandos
    description = 'El bot responderá al saludo indicado'  # Descripción del comando
    needArgument = False
    estado = False
    support_gestor = True
    support_voice = False
    def execute(self):
      print("Se ha ejecutado el comando")
    def activate(self, finger_positions):        
      if self.BOT.imageReconigtion.check_up_fingers(['thumb']) and \
           not self.BOT.imageReconigtion.check_up_fingers(['index', 'middle', 'ring', 'pinky']):
            return True
      else:
            return False

      
    def execute(self, *args):
        print("Pulgar")