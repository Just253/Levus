from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QPainterPath, QPalette, QBrush, QImage, QCursor
from screeninfo import get_monitors

def get_screen_resolution():
    """ Obtener la resolución de la pantalla (ancho, alto) """
    monitor = get_monitors()[0]
    return monitor.width, monitor.height

class DraggableRoundWindow(QWidget):
    def __init__(self, screen_width, screen_height, parent=None):
        super(DraggableRoundWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(85, 85)  # Set the size of the window
        self.dragging = False
        self.offset = QPoint()
        self.screen_width = screen_width
        self.screen_height = screen_height

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
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging: return self.move(event.globalPos() - self.offset)
        

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            half_screen_width = self.screen_width / 2
            quarter_window_width = self.width() / 4
            window_height = self.height()
            y = event.globalPos().y() - self.offset.y()

            # Para que la ventana no salga de la pantalla
            if y >= self.screen_height - window_height:
                y = self.screen_height - window_height
            elif y <= window_height:
                y = 0

            # Para que la ventana se acomode a la izquierda o derecha
            if event.globalPos().x() >= half_screen_width:
                x = self.screen_width - quarter_window_width
            else:
                x = quarter_window_width - self.width()

            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(500)  # Duración de la animación en milisegundos
            self.animation.setStartValue(QRect(self.pos(), self.size()))
            self.animation.setEndValue(QRect(QPoint(x, y), self.size()))
            self.animation.setEasingCurve(QEasingCurve.OutCubic)  # Cambiar la curva de la animación
            self.animation.start()

            

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    screen_width, screen_height = get_screen_resolution()
    window = DraggableRoundWindow(screen_width, screen_height)
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.move(window.width() / -2, screen_height / 2)
    window.show()
    sys.exit(app.exec())
