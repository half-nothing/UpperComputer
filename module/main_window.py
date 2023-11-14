from PyQt6.QtWidgets import QMainWindow

from form.generate.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_config_window(self, value):
        self.connect_config.setCurrentIndex(value)

