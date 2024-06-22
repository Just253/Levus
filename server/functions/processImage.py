from ..gestureRecognition.app import HandGestureRecognition
from ..commands.hide_all_windows import BotCommand as hide_all_windows
from ..commands.show_minimized_windows import BotCommand as show_minimized_windows
HGR = HandGestureRecognition()
import cv2
import time

def timer(last_time):
    current_time = time.time()
    if current_time - last_time > 5:
        return True, current_time
    return False, last_time

def processGesture(name, history, hand, last_time):
    if name is None or hand is None:
        return last_time

    name = name.lower()
    hand = hand.lower()

    if hand == 'left' and name == 'close':
        should_execute, new_time = timer(last_time)  # Calcula si debe ejecutar sin actualizar last_time aún
        if should_execute:
            print("Hidding all windows")
            hide_all_windows().execute()
            last_time = new_time  # Actualiza last_time solo si se ejecuta el comando

    if history is None:
        return last_time

    history = history.lower()
    if hand == 'right' and history == 'clockwise':
        should_execute, new_time = timer(last_time)  # Calcula si debe ejecutar sin actualizar last_time aún
        if should_execute:
            print("Showing all windows")
            show_minimized_windows().execute()
            last_time = new_time  # Actualiza last_time solo si se ejecuta el comando

    return last_time

def generate(debug_mode=False):
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    HGR.set_camera(cap)
    images = HGR.run()
    last_time = time.time()  # Inicializa last_time antes de comenzar el bucle
    try:
        for frame, info in images:
            try:
                actual_gesture, history_gesture, hand = info
                # Actualiza last_time con el valor devuelto por processGesture
                if not debug_mode:
                    last_time = processGesture(actual_gesture, history_gesture, hand, last_time)
                header = (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n'
                          b'Content-Length: ' + bytes(str(len(frame)), 'utf-8') + b'\r\n\r\n')
                footer = b'\r\n\r\n'
                yield header + frame + footer
            except Exception as e:
                print(e)
                break
    finally:
        print("Finishing")
        HGR.shutdown()
        print("Shutdown")