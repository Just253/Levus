import mediapipe as mp
import json
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

last_saved_time = time.time()

def save(hand_landmarks, filepath='landmarks.json'):
    global last_saved_time
    current_time = time.time()
    if current_time - last_saved_time >= 10:
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.append({
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z
            })
        with open(filepath, 'w') as f:
            json.dump(landmarks, f)
        print("### Landmarks ###")
        print(f"Landmarks saved to {filepath}")
        print("#################")
        last_saved_time = current_time