import cv2
import mediapipe as mp
import json

def load_landmarks(file_path='./tests/cam/landmarks.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def compare_landmarks(landmarks1, landmarks2, tolerance=0.1):
    for l1, l2 in zip(landmarks1, landmarks2):
        if (abs(l1['x'] - l2['x']) > tolerance or
            abs(l1['y'] - l2['y']) > tolerance or
            abs(l1['z'] - l2['z']) > tolerance):
            print(f"Diferencia encontrada: {(abs(l1['x'] - l2['x']), abs(l1['y'] - l2['y']), abs(l1['z'] - l2['z']))}")
            return False
    return True

saved_landmarks = load_landmarks()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
filter_on = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    original_image = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            current_landmarks = []
            for landmark in hand_landmarks.landmark:
                current_landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
            if compare_landmarks(saved_landmarks, current_landmarks):
                print("Mano en la misma posición")
                filter_on = False
            else:
                print("Mano en distinta posición")
                filter_on = True

    if filter_on:
        # Aplica el filtro a la imagen
        pass
    else:
        image = original_image

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()