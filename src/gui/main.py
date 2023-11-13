# TODO: FIX CHILD WIDGETS not showing out of the window

from typing import Optional
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QPainterPath, QPalette, QBrush, QImage, QCursor
from screeninfo import get_monitors
import os, sys
def get_screen_resolution():
    """ Obtener la resolución de la pantalla (ancho, alto) """
    monitor = get_monitors()[0]
    return monitor.width, monitor.height
def calculate_distance(self):
    """ Calcular la distancia entre el cursor y la ventana """
    cursor_pos = QCursor.pos()
    window_center_x = self.pos().x() + self.width() / 2
    window_center_y = self.pos().y() + self.height() / 2
    distance = ((cursor_pos.x() - window_center_x) ** 2 + (cursor_pos.y() - window_center_y) ** 2) ** 0.5
    return distance    

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def moveAnimation(self, x, y, duration):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(duration)  # Duración de la animación en milisegundos
        self.animation.setStartValue(QRect(self.pos(), self.size()))
        self.animation.setEndValue(QRect(QPoint(x, y), self.size()))
        self.animation.setEasingCurve(QEasingCurve.OutCubic)  # Cambiar la curva de la animación
        self.animation.start()

    def setup_background_image(self, image_path):
        image = QImage(image_path)
        if image.isNull():  raise Exception(f"Failed to load image: {image_path}")
        self.setAutoFillBackground(True)
        scaled_image = image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 100, 100)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(path, self.palette().window())    

class SideWidget(CustomWidget):
    def __init__(self, func = None, parent=None):
        super(SideWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(20, 20)
        self.setWindowOpacity(1)
        self.func = func
        self.show()    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.func: self.func()
    
class Coordinates:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

class DraggableRoundWindow(CustomWidget):
    def __init__(self, voice_toogle_func = None, cam_toogle_func = None, stop_func = None, parent=None):
        super(DraggableRoundWindow, self).__init__(parent)
        self.mic_widget = SideWidget(voice_toogle_func, self)
        self.cam_widget = SideWidget(cam_toogle_func, self)
        self.stop_func = stop_func
        self.setup_window()
        self.show()
        self.moveWidgetAnimation(self.cords.x, self.cords.y, 100)
        self.moveSideWidgets()

    def setup_window(self):
        self.setFixedSize(90, 90)  # Set the size of the window
        self.dragging = False
        self.ismoving = False
        self.cursor_over = False
        self.offset = QPoint()
        self.screen_width, self.screen_height = get_screen_resolution()
        self.cords = Coordinates()
        self.cords.x, self.cords.y = [self.width() / 4 - self.width() , self.screen_height / 2]
        self.toogle_window_opacity()

        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        image_path = os.path.join(parent_dir, "assets", "levus_logo.png")
        self.setup_background_image(image_path)

        mic_logo = os.path.join(parent_dir, "assets", "mic_logo.webp")
        cam_logo = os.path.join(parent_dir, "assets", "cam_logo.webp")
        self.mic_widget.setup_background_image(mic_logo)
        self.cam_widget.setup_background_image(cam_logo)

        self.moveSideWidgets()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.position()
        # TODO: Search another solution
        if event.button() == Qt.RightButton:
            if self.stop_func: self.stop_func()
            QApplication.instance().quit()

    def mouseMoveEvent(self, event):
        # TODO: fix window stop when press CTRL + SHIFT + S
        if self.dragging: self.ismoving = True
        if self.dragging and self.ismoving: 
            point = (event.globalPosition() - self.offset).toPoint()
            self.moveWidget(point.x(), point.y())
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.ismoving:
            self.dragging = False
            self.ismoving = False
            half_screen_width = self.screen_width / 2
            quarter_window_width = self.width() / 4
            window_height = self.height()
            y = event.globalPosition().y() - self.offset.y()

            # Para que la ventana no salga de la pantalla
            if y >= self.screen_height - window_height: # Abajo
                y = self.screen_height - window_height
            elif y <= window_height: # Arriba
                y = 0

            # Para que la ventana se acomode a la izquierda o derecha
            if event.globalPosition().x() >= half_screen_width: # Lado derecho
                x = self.screen_width - quarter_window_width
            else: # Lado contrario
                x = quarter_window_width - self.width()

            self.cords.x = x
            self.cords.y = y
            self.moveWidgetAnimation(x, y, 500)
            
    def enterEvent(self, event):
        if not self.cursor_over:
            self.cursor_over = True
            x = event.globalPosition().x() - self.offset.x()
            y = self.cords.y
            if x >= self.screen_width / 2: # Lado derecho
                x = self.screen_width - self.width()
            else: # Lado contrario
                x = 0
            # salga un poco de su zona para mostrarse
            self.moveWidgetAnimation(x, y, 500)
            self.toogle_window_opacity()

    def leaveEvent(self, event):
        # TODO: fix window loop
        if self.cursor_over:
            self.cursor_over = False
            self.moveWidgetAnimation(self.cords.x, self.cords.y, 500)
            self.toogle_window_opacity()
                  
    def moveWidgetAnimation(self, x, y, duration):
        self.moveAnimation(x, y, duration)
    
    def moveWidget(self, x, y):
        self.move(x, y)
        self.moveSideWidgets()
    
    def moveSideWidgets(self):
        self.mic_widget.move(self.width() / 6, self.height() / 2 + self.width() / 10)
        self.cam_widget.move(self.width() / 2 + self.width() / 10, self.height() / 2 + self.width() / 10)

    def toogle_window_opacity(self):
        if self.windowOpacity() != 1:
            self.setWindowOpacity(1)
        else:
            self.setWindowOpacity(0.2)

def startGui(voiceRecognitionToggle, imageRecognitionToggle, stopAll):
    app = QApplication(sys.argv)
    window = DraggableRoundWindow(voiceRecognitionToggle, imageRecognitionToggle, stopAll)
    sys.exit(app.exec())