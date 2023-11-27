import time
import cv2 as cv
import numpy as np
import mediapipe as mp
from screeninfo import get_monitors
from threading import Thread
from pynput.mouse import Controller
from src.gestureToTxt.fingers import *

class HandGesture:
    def __init__(self, BOT):
        from src.Levus import Levus
        self.BOT: Levus = BOT
        self.monitors = get_monitors()
        self.WIDTH = self.monitors[0].width if self.monitors else 1920
        self.HEIGHT = self.monitors[0].height if self.monitors else 1080
        self.cap = cv.VideoCapture(0)
        self.mouse = Controller()
        self.state = ''
        self.finger_positions = []
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                                              max_num_hands=1,
                                              min_tracking_confidence=0.5,
                                              min_detection_confidence=0.5)
        self.run = False
        

    def get_distance(self, c1, c2):
        x1, y1 = c1
        x2, y2 = c2
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2) 
        return distance

    def start(self):
        self.run = True
        self._run_recognition()
    def stop(self):
        self.run = False

    def _run_recognition(self):
        fps_limit = 1
        frame_period = 1/ fps_limit
        while self.run:
            start_time = time.time()
            state = ''
            success, frame = self.cap.read()
            if not success:
                break
            frame = cv.flip(frame, 4)
            result = self.hands.process(frame)
            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, handLms, mp.solutions.hands.HAND_CONNECTIONS)

                    finger_tips = {
                        'thumb': THUMB_TIP,
                        'index': INDEX_TIP,
                        'middle': MIDDLE_TIP,
                        'ring': RING_TIP,
                        'pinky': PINKY_TIP,
                    }

                    finger_positions = {}

                    for finger, tip in finger_tips.items():
                        finger_positions[finger] = [handLms.landmark[tip].x * self.WIDTH, handLms.landmark[tip].y * self.HEIGHT]
                    
                    finger_positions['palm'] = self.get_palm_position(handLms)
                    
                    self.setLastFingersPositions(finger_positions)
                    Thread(target=self.BOT.check_gesture_commands(finger_positions)).start()
            else:
                time_elapsed = time.time() - start_time
                if time_elapsed < frame_period:
                    time.sleep(frame_period - time_elapsed)
            
            cv.imshow('Camera', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv.destroyAllWindows()
    def getLastFingersPositions(self):
        return self.finger_positions
    def setLastFingersPositions(self,positions):
        self.finger_positions = positions
    def get_palm_position(self, handLms):
        palm_positions = [INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]

        x = sum(handLms.landmark[pos].x for pos in palm_positions) / len(palm_positions)
        y = sum(handLms.landmark[pos].y for pos in palm_positions) / len(palm_positions)

        return [x * self.WIDTH, y * self.HEIGHT]
    def check_up_fingers(self, fingers_up):
        finger_positions = self.getLastFingersPositions()
        # Lista de todos los dedos
        all_fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

        # Dedos que deberían estar abajo
        fingers_down = [finger for finger in all_fingers if finger not in fingers_up]

        # Comprobar si los dedos que deberían estar arriba están arriba
        if not all(finger_positions[finger][1] < finger_positions['palm'][1] for finger in fingers_up):
            return False

        # Comprobar si los dedos que deberían estar abajo están abajo
        if not all(finger_positions[finger][1] > finger_positions['palm'][1] for finger in fingers_down):
            return False

        return True

#if __name__ == '__main__':
#    gesture = HandGesture()
#    gesture.start()