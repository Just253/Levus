import cv2, time
import mediapipe as mp


def generate():
    cap = cv2.VideoCapture(cv2.CAP_ANY)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Inicializar MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
               max_num_hands=2,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir el color de BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar el frame para detectar las manos
        results = hands.process(frame_rgb)

        # Dibujar los puntos de la mano
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        new_frame_time = time.time()

        # Calcular el FPS
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # Convertir el FPS a cadena para visualizarlo
        fps_text = str(int(fps))

        # Poner el texto de FPS en el frame
        cv2.putText(frame, fps_text, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        try:
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n'
            b'Content-Length: ' + bytes(str(len(frame)), 'utf-8') + b'\r\n\r\n' +
            frame + b'\r\n\r\n')
        except:
            cap.release()
            hands.close()  # Asegúrate de cerrar el objeto hands
            return

    cap.release()
    hands.close()  # Asegúrate de cerrar el objeto hands