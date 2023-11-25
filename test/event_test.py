from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

    def mouseMoveEvent(self, event):
        pos = event.position()  # 或者使用 localPos() 方法
        x, y = pos.x(), pos.y()
        print(f"Mouse moved to ({x}, {y})")


app = QApplication([])
widget = MyWidget()
widget.show()
app.exec()