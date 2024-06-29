from ..gestureRecognition.app import HandGestureRecognition
from ..commands.hide_all_windows import BotCommand as hide_all_windows
from ..commands.show_minimized_windows import BotCommand as show_minimized_windows
HGR = HandGestureRecognition()
import cv2
import time
import pyautogui

def timer(last_time):
    current_time = time.time()
    if current_time - last_time > 2:
        return True, current_time
    return False, last_time

import ctypes
from ctypes import wintypes

# Constantes para eventos del mouse
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_ABSOLUTE = 0x8000

# Funciones de la API de Windows
SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event

# Estructura para la posición del cursor
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# Antes de la definición de la función processGesture, agregar:
screen_width, screen_height = pyautogui.size()
max_movement = min(screen_width, screen_height) // 10  # Límite máximo de movimiento
last_gesture = None  # Almacena el último gesto de movimiento
movement_speed = 5  # Velocidad inicial de movimiento

def adjust_movement_speed(name):
    global last_gesture, movement_speed
    if name == last_gesture:
        movement_speed = min(movement_speed + 2, max_movement)
    else:
        movement_speed = 5
    last_gesture = name


# Obtener la posición actual del cursor
def get_cursor_pos():
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def move_mouse(x, y):
    current_x, current_y = get_cursor_pos()
    SetCursorPos(current_x + x, current_y + y)

def click_mouse():
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def processGesture(name, history, hand, last_time):
    if name is None or hand is None:
        return last_time

    name = name.lower()
    hand = hand.lower()

    if hand == 'left' and name == 'close':
        should_execute, new_time = timer(last_time)
        if should_execute:
            print("Hidding all windows")
            hide_all_windows().execute()
            last_time = new_time

    if history is None:
        return last_time

    history = history.lower()
    if hand == 'right' and name == 'open':
        should_execute, new_time = timer(last_time)
        if should_execute:
            print("Showing all windows")
            show_minimized_windows().execute()
            last_time = new_time

    adjust_movement_speed(name)
    if name == 'mouse_up':
        move_mouse(0, -movement_speed)
    elif name == 'mouse_down':
        move_mouse(0, movement_speed)
    elif name == 'mouse_right':
        move_mouse(-movement_speed, 0)
    elif name == 'mouse_left':
        move_mouse(movement_speed, 0)

    if name == 'ok':
        should_execute, new_time = timer(last_time)
        if should_execute:
            click_mouse()
            last_time = new_time

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
        for frame, info,_ in images:
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