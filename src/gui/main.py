from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QPainterPath, QPalette, QBrush, QImage, QCursor
from screeninfo import get_monitors
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

class Coordinates:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

class DraggableRoundWindow(QWidget):
    def __init__(self, parent=None):
        super(DraggableRoundWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(90, 90)  # Set the size of the window
        self.toogle_window_opacity()
        self.dragging = False
        self.cursor_over = False
        self.offset = QPoint()
        self.screen_width, self.screen_height = get_screen_resolution()
        self.cords = Coordinates()
        self.cords.x, self.cords.y = [self.width() / 4 - self.width() , self.screen_height / 2]
        self.move(self.cords.x, self.cords.y)
        self.show()
        # Set the background image
        image_path = "assets/levus_logo.png"
        image = QImage(image_path)
        if image.isNull():
            raise Exception(f"Failed to load image: {image_path}")
        else:
            self.setAutoFillBackground(True)
            scaled_image = image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(scaled_image))
            self.setPalette(palette)

        # Create labels to display window position and mouse position
        self.window_position_label = QLabel()
        self.mouse_position_label = QLabel()

        # Create a layout and add the labels to it
        layout = QVBoxLayout()
        layout.addWidget(self.window_position_label)
        layout.addWidget(self.mouse_position_label)
        layout.addStretch()

        # Set the layout for the window
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 100, 100)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(path, self.palette().window())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.position()

    def mouseMoveEvent(self, event):
        # TODO: fix window stop when press CTRL + SHIFT + S
        if self.dragging: self.move((event.globalPosition() - self.offset).toPoint())
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
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
            self.moveAnimation(x, y, 500)
            

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
            self.moveAnimation(x, y, 500)
            self.toogle_window_opacity()

    def leaveEvent(self, event):
        # TODO: fix window loop
        if self.cursor_over:
            if self.dragging: return
            self.cursor_over = False
            self.moveAnimation(self.cords.x, self.cords.y, 500)
            self.toogle_window_opacity()
                  
    def moveAnimation(self, x, y, duration):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(duration)  # Duración de la animación en milisegundos
        self.animation.setStartValue(QRect(self.pos(), self.size()))
        self.animation.setEndValue(QRect(QPoint(x, y), self.size()))
        self.animation.setEasingCurve(QEasingCurve.OutCubic)  # Cambiar la curva de la animación
        self.animation.start()
    
    def toogle_window_opacity(self):
        if self.windowOpacity() != 1:
            self.setWindowOpacity(1)
        else:
            self.setWindowOpacity(0.5)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DraggableRoundWindow()
    sys.exit(app.exec())
