from flask_socketio import emit
from .. import socketio
import threading
import cv2, webcam
import time

def convert_to_bytes(image):
    # Comprime la imagen
    is_success, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    if is_success:
        return buffer.tobytes()
    else:
        return None

def transmit_camera_images(stop_event):
    cam = webcam.Webcam(src=0, max_frame_rate=30, run_in_background=False, w=1280, h=720)
    for frame in cam:
        print("Capturing frame")
        image_bytes = convert_to_bytes(frame)
        if image_bytes is not None:
            print("Transmitting image")
            socketio.emit('receiveImage', image_bytes)
        if stop_event.is_set():
          print("Stopping camera transmission")
          break

# Este es el hilo que ejecutará la función de transmisión
camera_thread = None
# Añadimos un evento de parada para señalar al hilo cuando debe parar
stop_event = threading.Event()

@socketio.on('toggleCam')
def cam(isOn):
  global camera_thread, stop_event
  if isOn is None:
    emit('error', {'error': 'No isOn provided'})
    return
  return 
  if isinstance(isOn, bool):
    if isOn:
      # Si isOn es True y el hilo de la cámara no está en ejecución, inicia el hilo
      if camera_thread is None or not camera_thread.is_alive():
        stop_event.clear()
        camera_thread = threading.Thread(target=transmit_camera_images, args=(stop_event,))
        camera_thread.start()
    else:
      # Si isOn es False y el hilo de la cámara está en ejecución, detén el hilo
      if camera_thread is not None and camera_thread.is_alive():
        stop_event.set()
  else:
    emit('error', {'error': 'isOn is not a boolean'})