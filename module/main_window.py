from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow

from form.generate.main_window import Ui_MainWindow
from module.utils.message_box import show_warn_box


class MainWindow(QMainWindow, Ui_MainWindow):
    _receive_in_hex: bool = False
    _send_in_hex: bool = False
    _items = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' ')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serial_config.receive_data_signal.connect(self._receive_data)
        self.serial_config.clear_receive_data_signal.connect(self.receive_text.clear)
        self.serial_config.serial_open_signal.connect(self._connection_open)
        self.serial_config.show_in_hex_signal.connect(self._receive_show_in_hex)
        self.serial_config.clear_total_data_signal.connect(self.soft_status.clear)

    def _connection_open(self, status: bool):
        self.connect_config_select.setEnabled(status)
        self.soft_status.connect_status_text.setText("未连接" if status else "已连接")
        self.single_send.setEnabled(not status)

    def update_config_window(self, value):
        self.connect_config.setCurrentIndex(value)

    def _receive_data(self, data: bytes, size: int):
        if not data:
            return
        self.soft_status.total_receive_change_signal.emit(size)
        match self.tabWidget.currentIndex():
            case 0:
                if self.serial_config.auto_send_back.isChecked():
                    self.serial_config.serial.send(data)
                if self.serial_config.show_in_hex.isChecked():
                    data = ' '.join(hex(c)[2:] for c in data) + ' '
                else:
                    try:
                        data = data.decode("utf-8")
                    except UnicodeDecodeError:
                        try:
                            data = data.decode("gbk")
                        except UnicodeDecodeError:
                            data = repr(data).lstrip('b').strip('\'').replace("\\x", "")
                            data = ' '.join(data[i:i + 2] for i in range(0, len(data), 2)) + ' '
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

    def send_data(self):
        data = self.single_send_text.toPlainText()
        if not data:
            return
        if self.serial_config.send_new_line.isChecked():
            data += '\r\n'
        if self.serial_config.show_back.isChecked():
            self.receive_text.insertPlainText(data)
        if self.single_send_in_hex.isChecked():
            data = data.replace(" ", "")
            for item in data:
                if item.upper() not in self._items:
                    show_warn_box("警告", f"字符\"{item}\"不是有效的十六进制字符([0-9, A-F])")
                    return
            if len(data) & 1:
                data += '0'
            data = bytes.fromhex(data)
        else:
            data = ' '.join(fr"{c:02x}" for c in data.encode("gbk" if self.encoding_in_gbk.isChecked() else "utf-8"))
            data = bytes.fromhex(data)
        length = len(data)
        match (self.connect_config.currentIndex()):
            case 0:
                self.serial_config.serial.send(data)
            case 1:
                pass
            case 2:
                pass
        self.soft_status.total_send_change_signal.emit(length)
        if self.serial_config.clear_after_send.isChecked():
            self.single_send_text.clear()

    def send_show_in_hex(self):
        checked = self.single_send_in_hex.isChecked()
        data = self.single_send_text.toPlainText()
        if checked and checked != self._send_in_hex:
            self._send_in_hex = checked
            data = ' '.join(fr"{c:02x}" for c in data.encode("gbk" if self.encoding_in_gbk.isChecked() else "utf-8"))
            self.single_send_text.setPlainText(data)
        if not checked and checked != self._send_in_hex:
            for item in data:
                if item.upper() not in self._items:
                    show_warn_box("警告", f"字符\"{item}\"不是有效的十六进制字符([0-9, A-F])")
                    return
            try:
                if self.encoding_in_gbk.isChecked():
                    self.single_send_text.setPlainText(bytes.fromhex(data).decode('gbk'))
                else:
                    self.single_send_text.setPlainText(bytes.fromhex(data).decode('utf-8'))
            except UnicodeDecodeError:
                data = repr(bytes.fromhex(data)).lstrip('b').strip('\'').replace("\\x", "")
                data = ' '.join(data[i:i + 2] for i in range(0, len(data), 2))
                self.single_send_text.setPlainText(data)
            self._send_in_hex = checked

    def _receive_show_in_hex(self, show_in_hex: bool):
        if show_in_hex:
            if show_in_hex != self._receive_in_hex:
                text = self.receive_text.toPlainText()
                self.receive_text.clear()
                self.receive_text.setPlainText(' '.join(hex(c)[2:] for c in text.encode()) + ' ')
                self._receive_in_hex = show_in_hex
        else:
            if show_in_hex != self._receive_in_hex:
                text = self.receive_text.toPlainText().strip()
                self._receive_in_hex = show_in_hex
                try:
                    self.receive_text.setPlainText(bytes.fromhex(text).decode('utf-8'))
                except UnicodeDecodeError:
                    try:
                        self.receive_text.setPlainText(bytes.fromhex(text).decode('gbk'))
                    except UnicodeDecodeError:
                        self.receive_text.setPlainText(repr(bytes.fromhex(text)))
