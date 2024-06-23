from server.gestureRecognition.app import HandGestureRecognition
import cv2

cv = cv2.VideoCapture(0, cv2.CAP_DSHOW)
hg = HandGestureRecognition()
hg.set_camera(cv)
images = hg.run()
for image,_,_ in images:
    cv2.imshow('frame', _)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Instrucciones 
# teclas
# k = modo grabar keypoint (imagenes estaticas)
# h = modo grabar point_history | No usar en este caso
# n = desactivar grabacion
# esc/q = salir

# Elegir un numero del 1-9 (en este caso 1-3 ya estan ocupados) para grabar con ese ID y presionar ese numero

# !!! el cv2 no logra detectar las teclas asi que repite la tecla varias veces (recuerda tener seleccionado la ventana de la camara)