import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from module.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    application.setWindowIcon(QIcon('./icon/icon.ico'))
    application.show()
    sys.exit(app.exec())
