from ..gestureRecognition.app import HandGestureRecognition
HGR = HandGestureRecognition()
import cv2
def generate():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    HGR.set_camera(cap)
    images = HGR.run()
    for frame in images:
        try:
            header = (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n'
                      b'Content-Length: ' + bytes(str(len(frame)), 'utf-8') + b'\r\n\r\n')
            footer = b'\r\n\r\n'
            yield header + frame + footer
        except Exception as e:
            print(e)
            break
    HGR.shutdown()