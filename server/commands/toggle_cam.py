from .command import Command
from .. import socketio

class BotCommand(Command):
  name = "toggle_cam"
  description = "Toggles the camera on and off"
  def execute(self, value: bool):
    """
    :param value: Enable/Disable the camera
    :type value: boolean
    """
    if type(value) is not bool:
        if value.lower() in ['true', '1']:
            value = True
        elif value.lower() in ['false', '0']:
            value = False
        else:
            return "Invalid value"
    socketio.emit('ToggleCam', value)
    return "Camera toggled"