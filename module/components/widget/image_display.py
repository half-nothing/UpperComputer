from typing import Optional

from PyQt6.QtCore import QLineF, QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QPen, QPixmap, QResizeEvent, QWheelEvent
from PyQt6.QtWidgets import QWidget

from form.generate.image_display import Ui_ImageDisplay


class ImageDisplay(QWidget, Ui_ImageDisplay):
    _start_point: QPointF = QPointF()
    _image_width: int = 188
    _image_height: int = 120
    _displayImage: QPixmap
    _mouse_pre_pos: QPointF
    _now_mouse_image_pos: QPointF
    _width_per_pix: float = 4
    _left_mouse_pressed: bool = False
    _zoom: float = 1

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._start_point.setX(0)
        self._start_point.setY(0)
        self._displayImage = QPixmap(self.image_width, self.image_height)
        self._displayImage.fill(QColor(30, 30, 30))
        self._now_mouse_image_pos = self._start_point
        self.setMouseTracking(True)

    def resizeEvent(self, event: QResizeEvent):
        self.repaint()

    def display_image(self, image: QPixmap):
        if image.width() != self.image_width or image.height() != self.image_height:
            return
        self._displayImage = image
        self.repaint()

    def print_grid(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        lines: list[QLineF] = []
        x = self._start_point.x()
        while x <= self._start_point.x() + self._width_per_pix * self.image_width:
            lines.append(
                QLineF(x, self._start_point.y(), x, self._start_point.y() + self._width_per_pix * self.image_height))
            x += self._width_per_pix
        y: float = self._start_point.y()
        while y <= self._start_point.y() + self._width_per_pix * self.image_height:
            lines.append(
                QLineF(self._start_point.x(), y, self._start_point.x() + self._width_per_pix * self.image_width, y))
            y += self._width_per_pix
        painter.drawLines(lines)

    def get_rel_pos(self, pos: QPointF) -> QPointF:
        tmp: QPointF = pos - self._start_point
        return tmp / self._width_per_pix

    def draw_pixel(self, x: int, y: int, color: QColor) -> None:
        if x < 0 or y < 0 or x >= self.image_width or y >= self.image_height:
            return
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.setBrush(color)
        pixel_area = QRectF(self._start_point.x() + x * self._width_per_pix,
                            self._start_point.y() + y * self._width_per_pix, self._width_per_pix,
                            self._width_per_pix)
        painter.drawRect(pixel_area)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.drawPixmap(int(self._start_point.x()), int(self._start_point.y()),
                           int(self.image_width * self._width_per_pix),
                           int(self.image_height * self._width_per_pix), self._displayImage)
        self.draw_pixel(int(self._now_mouse_image_pos.x()), int(self._now_mouse_image_pos.y()),
                        QColor(255, 174, 201))
        self.print_grid()

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self._zoom += 0.1
            self._width_per_pix = 4 * self._zoom
        else:
            self._zoom -= 0.1
            if self._zoom < 1.0:
                self._zoom = 1.0
            self._width_per_pix = 4 * self._zoom
        self.repaint()

    def mouseMoveEvent(self, event: QMouseEvent):
        now_pos = event.position()
        tmp = self.get_rel_pos(now_pos)

        if tmp != self._now_mouse_image_pos:
            self._now_mouse_image_pos = tmp
            self.mouse_pos.setText(
                "图像坐标:(%d,%d)" % (int(self._now_mouse_image_pos.x()), int(self._now_mouse_image_pos.y())))
            self.repaint()

        if self._left_mouse_pressed:
            self._start_point += now_pos - self._mouse_pre_pos
            self.repaint()
            self._mouse_pre_pos = now_pos

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._left_mouse_pressed = True
            self._mouse_pre_pos = event.position()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._left_mouse_pressed = False

    def show_mouse_pos(self, status: bool):
        if status:
            self.mouse_pos.setVisible(True)
            return
        self.mouse_pos.setVisible(False)
        self.repaint()

    def image_height_change(self, height: str):
        self.image_height = int(height)

    def image_width_change(self, width: str):
        self.image_width = int(width)

    @property
    def image_width(self) -> int:
        return self._image_width

    @image_width.setter
    def image_width(self, value: int) -> None:
        self._image_width = value
        self.repaint()

    @property
    def image_height(self) -> int:
        return self._image_height

    @image_height.setter
    def image_height(self, value: int) -> None:
        self._image_height = value
        self.repaint()
