from threading import Event, Thread

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow

from form.generate.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serial_config.data_changed.connect(self.receive_data)
        self.serial_config.clear_receive_data_signal.connect(self.clear_receive_data)

    def update_config_window(self, value):
        self.connect_config.setCurrentIndex(value)

    def receive_data(self, data, size):
        self.receive_text.insertPlainText(data)
        self.soft_status.total_receive_change_signal.emit(size)

    def scroll_to_bottom(self):
        self.receive_text.moveCursor(QTextCursor.MoveOperation.End)

    def clear_receive_data(self):
        self.receive_text.clear()