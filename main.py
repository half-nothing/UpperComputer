import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import QApplication, QStyleFactory

from module.main_window import MainWindow
from module.utils.path_solve import get_resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path('resource/icon/icon.ico')))
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Shadow, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(142, 45, 197))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(87, 87, 87))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(54, 54, 54))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(54, 54, 54))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(54, 54, 54))
    app.setPalette(palette)
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
