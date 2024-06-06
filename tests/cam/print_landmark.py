import cv2
import mediapipe as mp
from save_landmark import save
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
last_saved_time = time.time()

while (cap.isOpened()):
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for idx, landmark in enumerate(hand_landmarks.landmark):
                print(f"Landmark {idx}: (X: {landmark.x}, Y: {landmark.y}, Z: {landmark.z})")
            current_time = time.time()
            if current_time - last_saved_time >= 10: 
                save(hand_landmarks, './tests/cam/landmarks.json')
                last_saved_time = current_time # Carita enojada carita enojada

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()