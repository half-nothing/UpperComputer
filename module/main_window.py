from threading import Event, Thread

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow

from form.generate.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    in_hex: bool = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serial_config.data_changed.connect(self.receive_data)
        self.serial_config.clear_receive_data_signal.connect(self.receive_text.clear)
        self.serial_config.serial_open_signal.connect(lambda status: self.connect_config_select.setEnabled(status))
        self.serial_config.serial_open_signal.connect(
            lambda status: self.soft_status.connect_status_text.setText("未连接" if status else "已连接"))

    def update_config_window(self, value):
        self.connect_config.setCurrentIndex(value)

    def receive_data(self, data: str, size: int, show_in_hex: bool):
        if not data:
            return
        self.soft_status.total_receive_change_signal.emit(size)
        if show_in_hex:
            data = ' ' + (' '.join(hex(ord(c))[2:] for c in data))
            if show_in_hex != self.in_hex:
                text = self.receive_text.toPlainText()
                self.receive_text.clear()
                self.receive_text.setPlainText(' '.join(hex(ord(c))[2:] for c in text))
                self.in_hex = show_in_hex
        else:
            if show_in_hex != self.in_hex:
                text = self.receive_text.toPlainText().strip()
                self.receive_text.setPlainText(bytes.fromhex(text).decode('utf-8'))
                self.in_hex = show_in_hex
        match self.tabWidget.currentIndex():
            case 0:
                self.receive_text.insertPlainText(data)
            case 1:
                pass
            case 2:
                pass

    def scroll_to_bottom(self):
        self.receive_text.moveCursor(QTextCursor.MoveOperation.End)

    def update_clear_button(self, index: int):
        match index:
            case 0:
                self.serial_config.clear_receive_area_button.setEnabled(True)
            case 1 | 2:
                self.serial_config.clear_receive_area_button.setEnabled(False)
