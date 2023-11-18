import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from module.main_window import MainWindow
from module.utils.path_solve import get_resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    application.setWindowIcon(QIcon(get_resource_path('./icon/icon.ico')))
    application.show()
    sys.exit(app.exec())
