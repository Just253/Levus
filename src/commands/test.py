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
      self.estado = True
      # Si la posición y del pulgar es menor que la de los otros dedos por un cierto umbral, consideramos que el pulgar está levantado
      return  self.BOT.imageReconigtion.check_up_fingers(['thumb'])
      #if finger_positions['thumb'][1] < finger_positions['index'][1] - 50 and \
      #  finger_positions['thumb'][1] < finger_positions['middle'][1] - 50 and \
      #  finger_positions['thumb'][1] < finger_positions['ring'][1] - 50 and \
      #  finger_positions['thumb'][1] < finger_positions['pinky'][1] - 50:
      #    return True
      #else:
      #    return False
      
    def execute(self, *args):
        print("Pulgar")