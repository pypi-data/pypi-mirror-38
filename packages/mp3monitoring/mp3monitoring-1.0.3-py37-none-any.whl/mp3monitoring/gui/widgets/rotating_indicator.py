from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget


class RotatingIndicator(QWidget):
    def __init__(self, parent=None):
        super(RotatingIndicator, self).__init__(parent)
        self.parent = parent

        self.timer = None
        self.degree = 0
        self.radius = 100
        self.circle_width = 10
        self.rotate_length = 5760 / 360 * 45  # 1/16 degree
        self.speed = 10  # 1/16 degree
        self.background_color = QColor(255, 255, 255, 200)
        self.rotate_color = QColor(255, 0, 0, 200)

        size = int(self.radius + self.circle_width / 2 + 20)
        self.setMinimumSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        x_mid, y_mid = self.get_middle_point(self.radius)

        # background circle
        pen = QPen()
        pen.setWidth(self.circle_width)
        pen.setColor(self.background_color)
        painter.setPen(pen)
        painter.drawArc(x_mid, y_mid, self.radius, self.radius, 0, 5760)

        # rotate circle
        pen = QPen()
        pen.setWidth(self.circle_width)
        pen.setColor(self.rotate_color)
        painter.setPen(pen)
        start_degree = self.degree
        painter.drawArc(x_mid, y_mid, self.radius, self.radius, -start_degree, self.rotate_length)

    def showEvent(self, event):
        self.timer = self.startTimer(5)
        self.degree = 0

    def timerEvent(self, event):
        self.degree = (self.degree + self.speed) % 5760
        self.update()

    def get_middle_point(self, outer_radius):
        return self.width() / 2 - outer_radius / 2, self.height() / 2 - outer_radius / 2
