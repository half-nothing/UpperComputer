import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from module.main_window import MainWindow
from module.utils.path_solve import get_resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path('resource/icon/icon.ico')))
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
