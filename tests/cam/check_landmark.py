import cv2
import mediapipe as mp
import json
import math

def load_landmarks(file_path='c:\\Users\\Hans\\Levus\\tests\\cam\\landmarks.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def compare_landmarks(landmarks1, landmarks2, tolerance=0.01):
    for l1, l2 in zip(landmarks1, landmarks2):
        if (abs(l1['x'] - l2['x']) > tolerance or
            abs(l1['y'] - l2['y']) > tolerance or
            abs(l1['z'] - l2['z']) > tolerance):
            return False
    return True

saved_landmarks = load_landmarks()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

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

            if compare_landmarks(current_landmarks, saved_landmarks):
                print("Mano en la misma posición")
            else:
                print("Mano en distinta posición")

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
