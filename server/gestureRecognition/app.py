#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import argparse
import itertools
import os
import math
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp

from .utils import CvFpsCalc
from .model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from .model.point_history_classifier.point_history_classifier import PointHistoryClassifier

current_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(current_dir, 'model')
class HandGestureRecognition:
    def __init__(self,**kwargs):
        self.cap_width = kwargs.get('width', 960)
        self.cap_height = kwargs.get('height', 540)
        self.use_static_image_mode = kwargs.get('use_static_image_mode', False)
        self.min_detection_confidence = kwargs.get('min_detection_confidence', 0.7)
        self.min_tracking_confidence = kwargs.get('min_tracking_confidence', 0.5)
        self.use_brect = True
        self.running = True
        self.load_models()
        self.load_labels()
        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)
        self.finger_gesture_history = deque(maxlen=self.history_length)
        self.cvFpsCalc = CvFpsCalc(buffer_len=10)
    def set_camera(self, cv_cap):
        self.cap = cv_cap
        self.setup_camera()

    def setup_camera(self):
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)

    def load_models(self):
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(
            static_image_mode=self.use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        self.keypoint_classifier = KeyPointClassifier()
        self.point_history_classifier = PointHistoryClassifier()

    def load_labels(self):
        kc_label_path = os.path.join(model_dir, 'keypoint_classifier/keypoint_classifier_label.csv')
        phc_label_path = os.path.join(model_dir, 'point_history_classifier/point_history_classifier_label.csv')
        with open(kc_label_path, encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = [row[0] for row in csv.reader(f)]
        with open(phc_label_path, encoding='utf-8-sig') as f:
            self.point_history_classifier_labels = [row[0] for row in csv.reader(f)]

    def calculate_velocity(self,current_landmark, previous_landmark):
        if previous_landmark is None:
            return 0
        distance = math.sqrt((current_landmark[0] - previous_landmark[0]) ** 2 + (current_landmark[1] - previous_landmark[1]) ** 2)
        return distance
    
    def calc_center_of_hand(self, landmarks):
        x_coords = [landmark.x for landmark in landmarks.landmark]
        y_coords = [landmark.y for landmark in landmarks.landmark]

        # Calcula el centro como el promedio de las coordenadas x e y
        center_x = np.mean(x_coords)
        center_y = np.mean(y_coords)

        return (center_x, center_y)

    def run(self):
        self.running = True
        mode = 0
        number = -1
        smoothed_landmarks = {}
        alpha = 0.5
        previous_center_point = None
        while self.running:
            fps = self.cvFpsCalc.get()
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break
            _number, mode = select_mode(key, mode,number)
            number = _number if _number != number else number
            ret, image = self.cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)  # ミラー表示
            debug_image = copy.deepcopy(image)

            # 検出実施 #############################################################
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            hand_sign_text = None
            finger_gesture_text = None
            hand = None

            #  ####################################################################
            if results.multi_hand_landmarks is not None:
                for hand_index, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):

                    # Cálculo del centro de la mano como ejemplo
                    center_point = self.calc_center_of_hand(hand_landmarks)
                    velocity = self.calculate_velocity(center_point, previous_center_point)
                    previous_center_point = center_point
                    # Ajustar alpha basado en la velocidad
                    # Nota: Ajusta los valores 0.1 y 0.9 según sea necesario para tu aplicación
                    alpha = max(0.1, min(0.9, 1 - velocity / 10))

                    # 外接矩形の計算
                    hand = handedness.classification[0].label[0:]
                    brect = calc_bounding_rect(debug_image, hand_landmarks)
                    # ランドマークの計算
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                    # Aplicar suavizado
                    if hand_index not in smoothed_landmarks:
                        smoothed_landmarks[hand_index] = landmark_list  # Inicializar si es la primera vez
                    else:
                        for i, point in enumerate(landmark_list):
                            smoothed_landmarks[hand_index][i] = [
                                alpha * point[0] + (1 - alpha) * smoothed_landmarks[hand_index][i][0],
                                alpha * point[1] + (1 - alpha) * smoothed_landmarks[hand_index][i][1]
                            ]

                    landmark_list = smoothed_landmarks[hand_index]
                    # 相対座標・正規化座標への変換
                    pre_processed_landmark_list = pre_process_landmark(
                        landmark_list)
                    pre_processed_point_history_list = pre_process_point_history(
                        debug_image, self.point_history)
                    # 学習データ保存
                    logging_csv(number, mode, pre_processed_landmark_list,
                                pre_processed_point_history_list)

                    # ハンドサイン分類
                    hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                    if hand_sign_id == 2:  # 指差しサイン
                        self.point_history.append(landmark_list[8])  # 人差指座標
                    else:
                        self.point_history.append([0, 0])

                    # フィンガージェスチャー分類
                    finger_gesture_id = 0
                    point_history_len = len(pre_processed_point_history_list)
                    if point_history_len == (self.history_length * 2):
                        finger_gesture_id = self.point_history_classifier(
                            pre_processed_point_history_list)

                    # 直近検出の中で最多のジェスチャーIDを算出
                    self.finger_gesture_history.append(finger_gesture_id)
                    most_common_fg_id = Counter(
                        self.finger_gesture_history).most_common()

                    hand_sign_text = self.keypoint_classifier_labels[hand_sign_id]
                    finger_gesture_text = self.point_history_classifier_labels[most_common_fg_id[0][0]]

                    # 描画
                    debug_image = draw_bounding_rect(self.use_brect, debug_image, brect)
                    debug_image = draw_landmarks(debug_image, landmark_list)
                    debug_image = draw_info_text(
                        debug_image,
                        brect,
                        handedness,
                        hand_sign_text,
                        finger_gesture_text,
                    )
            else:
                self.point_history.append([0, 0])

            debug_image = draw_point_history(debug_image, self.point_history)
            debug_image = draw_info(debug_image, fps, mode, number)

            # 画面反映 #############################################################
            # to jpg
            _, jpg = cv.imencode('.jpg', debug_image)
            yield jpg.tobytes() , [hand_sign_text, finger_gesture_text, hand], debug_image
            #cv.imshow('Hand Gesture Recognition', debug_image)
    def shutdown(self):
        self.running = False
        self.cap.release()

def select_mode(key, mode, number):
    if 97 <= key <= 122:  # a-z
        number = key - 97
    if key == 57:  # 9
        mode = 0
    if key == 49:  # 1
        mode = 1
    if key == 50:  # 2
        mode = 2
    return number, mode

def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # キーポイント
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # 相対座標に変換
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # 1次元リストに変換
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # 正規化
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def pre_process_point_history(image, point_history):
    image_width, image_height = image.shape[1], image.shape[0]

    temp_point_history = copy.deepcopy(point_history)

    # 相対座標に変換
    base_x, base_y = 0, 0
    for index, point in enumerate(temp_point_history):
        if index == 0:
            base_x, base_y = point[0], point[1]

        temp_point_history[index][0] = (temp_point_history[index][0] -
                                        base_x) / image_width
        temp_point_history[index][1] = (temp_point_history[index][1] -
                                        base_y) / image_height

    # 1次元リストに変換
    temp_point_history = list(
        itertools.chain.from_iterable(temp_point_history))

    return temp_point_history


def logging_csv(number, mode, landmark_list, point_history_list):
    if mode == 0:
        pass
    if mode == 1 and 0 <= number:
        csv_path = os.path.join(model_dir, 'keypoint_classifier/keypoint.csv')
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
    if mode == 2 and 0 <= number:
        csv_path = os.path.join(model_dir, 'point_history_classifier/point_history.csv')
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *point_history_list])
    return
def draw_landmarks(image, landmark_point):
    color_negro = (0, 0, 0)
    color_blanco = (255, 255, 255)
    # Definir las conexiones usando un diccionario
    connections = {
        # indice
        2: [3, 5],
        3: [4],
        # dedo medio
        5: [6, 9],
        6: [7],
        7: [8],
        # anular
        9: [10, 13],
        10: [11],
        11: [12],
        # meñique
        13: [14, 17],
        14: [15],
        15: [16],
        # pulgar
        17: [18, 0],
        18: [19],
        19: [20],
        #palma
        0: [1],
        1: [2]
    }

    if landmark_point:
        for k, v_list in connections.items():
            for v in v_list:
                # Convertir las coordenadas a enteros
                start_point = tuple(map(int, landmark_point[k]))
                end_point = tuple(map(int, landmark_point[v]))
                cv.line(image, start_point, end_point, color_negro, 6)
                cv.line(image, start_point, end_point, color_blanco, 2)

    # Simplificar el dibujo de los círculos
    for index, landmark in enumerate(landmark_point):
        # Determinar el tamaño del círculo basado en el índice
        size = 8 if index in [4, 8, 12, 16, 20] else 5
        # Convertir las coordenadas a enteros
        center = tuple(map(int, landmark))
        cv.circle(image, center, size, color_blanco, -1)
        cv.circle(image, center, size, color_negro, 1)
    return image

def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # 外接矩形
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 1)

    return image


def draw_info_text(image, brect, handedness, hand_sign_text,
                   finger_gesture_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    if finger_gesture_text != "":
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                   cv.LINE_AA)

    return image


def draw_point_history(image, point_history):
    return image
    for index, point in enumerate(point_history):
        # Asegurarse de que point contiene valores numéricos
        if isinstance(point[0], (int, float)) and isinstance(point[1], (int, float)):
            # Convertir a enteros
            center = (int(point[0]), int(point[1]))
            cv.circle(image, center, 1 + int(index / 2), (152, 251, 152), 2)
    return image


def draw_text_with_outline(image, text, position, font, font_scale, font_thickness, text_color, outline_color, outline_thickness):
  # Dibuja el texto con contorno
  cv.putText(image, text, position, font, font_scale, outline_color, font_thickness + outline_thickness, cv.LINE_AA)
  cv.putText(image, text, position, font, font_scale, text_color, font_thickness, cv.LINE_AA)

def draw_info(image, fps, mode, number):
  # Simplifica el dibujo de información en la imagen
  draw_text_with_outline(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, 2, (255, 255, 255), (0, 0, 0), 2)

  mode_string = ['Logging Key Point', 'Logging Point History']
  if 1 <= mode <= 2:
    draw_text_with_outline(image, "MODE:" + mode_string[mode - 1], (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.6, 1, (255, 255, 255), (0, 0, 0), 2)
    if 0 <= number:
      draw_text_with_outline(image, "NUM:" + str(number), (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.6, 1, (255, 255, 255), (0, 0, 0), 2)
  return image