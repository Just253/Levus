import cv2
import time

# Define la captura de video
cap = cv2.VideoCapture(0)

# Configura la resolución de la cámara a 1280x720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Configura la tasa de fotogramas de la cámara a 30 FPS
cap.set(cv2.CAP_PROP_FPS, 30)

try:
    while True:
        # Comienza a contar el tiempo para este fotograma
        start_time = time.time()

        # Captura un fotograma de la cámara
        ret, frame = cap.read()

        # Muestra el fotograma en una ventana
        cv2.imshow('Webcam Frame', frame)

        # Calcula el tiempo que deberíamos esperar hasta el próximo fotograma
        time_to_next_frame = (1 / 30) - (time.time() - start_time)

        # Espera hasta el próximo fotograma o hasta que el usuario presione la tecla 'q'
        if cv2.waitKey(max(1, int(time_to_next_frame * 1000))) & 0xFF == ord('q'):
            break
finally:
    # Libera la cámara y destruye todas las ventanas de OpenCV
    cap.release()
    cv2.destroyAllWindows()