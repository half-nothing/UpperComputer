import sys

from PyQt6.QtWidgets import QApplication

from module.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
