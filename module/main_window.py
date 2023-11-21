from concurrent.futures import Future
from threading import Event, Thread
from time import sleep
from typing import BinaryIO, Optional, Union

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QFileDialog, QMainWindow
from serial.serialutil import EIGHTBITS, SEVENBITS, SIXBITS
from serial.serialutil import PARITY_EVEN, PARITY_NONE, PARITY_ODD
from serial.serialutil import STOPBITS_ONE, STOPBITS_TWO

from form.generate.main_window import Ui_MainWindow
from module.sockets.tcp_client import TCPClient
from module.sockets.tcp_server import TCPServer
from module.sockets.udp_client import UDPClient
from module.sockets.udp_server import UDPServer
from module.utils.message_box import show_warn_box
from module.utils.serial_manager import SerialManager
from module.utils.thread_pool_manager import thread_pool


class MainWindow(QMainWindow, Ui_MainWindow):
    _receive_in_hex: bool = False
    _send_in_hex: bool = False
    _items = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' ')
    _serial: Optional[SerialManager] = None
    _serial_read_data_thread: Optional[Future] = None
    _serial_read_data_thread_alive: Event = Event()
    _save_file: Optional[BinaryIO] = None
    _udp_socket: Optional[Union[UDPClient, UDPServer]] = None
    _tcp_socket: Optional[Union[TCPClient, TCPServer]] = None

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

    def save_data_to_file(self, status: bool):
        if status:
            file_path, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "", "所有文件 (*.*)")
            if file_path:
                self.file_path_edit.setEnabled(True)
                self.file_path_edit.setText(file_path)
                self._save_file = open(file_path, "wb+")
            return
        self.file_path_edit.setEnabled(False)
        self.file_path_edit.clear()
        self._save_file.close()
        self._save_file = None

    def update_config_window(self, value: int) -> None:
        match value:
            case 0:
                self.open_connection_button.setText("打开串口")
            case 1 | 2:
                self.open_connection_button.setText("打开连接")
        self.connect_config_stack_widget.setCurrentIndex(value)

    def _receive_data(self, data: bytes, size: int) -> None:
        if not data:
            return
        self.soft_status.total_receive_change_signal.emit(size)
        if self.save_to_file:
            self._save_file.write(data)
            self._save_file.flush()
        match self.main_area_widget.currentIndex():
            case 0:
                if self.send_back:
                    self._serial.send(data)
                if self.show_in_hex:
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
                self.receive_data_plain_edit.insertPlainText(data)
            case 1:
                pass
            case 2:
                pass

    def scroll_to_bottom(self) -> None:
        self.receive_data_plain_edit.moveCursor(QTextCursor.MoveOperation.End)

    def update_clear_button(self, index: int) -> None:
        match index:
            case 0:
                self.clear_receive_area_button.setEnabled(True)
            case 1 | 2:
                self.clear_receive_area_button.setEnabled(False)

    def send_data(self) -> None:
        data = self.single_send_text_plain_edit.toPlainText()
        if not data:
            return
        if self.send_new_line:
            data += '\r\n'
        if self.show_back:
            self.receive_data_plain_edit.insertPlainText(data)
        if self.single_send_in_hex:
            data = data.replace(" ", "")
            for item in data:
                if item.upper() not in self._items:
                    show_warn_box("警告", f"字符\"{item}\"不是有效的十六进制字符([0-9, A-F])")
                    return
            if len(data) & 1:
                data += '0'
            data = bytes.fromhex(data)
        else:
            data = ' '.join(
                fr"{c:02x}" for c in data.encode("gbk" if self.gbk_encoding else "utf-8"))
            data = bytes.fromhex(data)
        length = len(data)
        match (self.connect_config_combo_box.currentIndex()):
            case 0:
                self._serial.send(data)
            case 1:
                pass
            case 2:
                pass
        self.soft_status.total_send_change_signal.emit(length)
        if self.clear_after_send:
            self.single_send_text_plain_edit.clear()

    def send_show_in_hex(self, checked: bool) -> None:
        data = self.single_send_text_plain_edit.toPlainText()
        if checked and checked != self._send_in_hex:
            self._send_in_hex = checked
            data = ' '.join(
                fr"{c:02x}" for c in data.encode("gbk" if self.gbk_encoding else "utf-8"))
            self.single_send_text_plain_edit.setPlainText(data)
        if not checked and checked != self._send_in_hex:
            for item in data:
                if item.upper() not in self._items:
                    show_warn_box("警告", f"字符\"{item}\"不是有效的十六进制字符([0-9, A-F])")
                    return
            try:
                if self.gbk_encoding:
                    self.single_send_text_plain_edit.setPlainText(bytes.fromhex(data).decode('gbk'))
                else:
                    self.single_send_text_plain_edit.setPlainText(bytes.fromhex(data).decode('utf-8'))
            except UnicodeDecodeError:
                data = repr(bytes.fromhex(data)).lstrip('b').strip('\'').replace("\\x", "")
                data = ' '.join(data[i:i + 2] for i in range(0, len(data), 2))
                self.single_send_text_plain_edit.setPlainText(data)
            self._send_in_hex = checked

    def receive_show_in_hex(self, checked: bool) -> None:
        if checked:
            if checked != self._receive_in_hex:
                text = self.receive_data_plain_edit.toPlainText()
                self.receive_data_plain_edit.setPlainText(' '.join(hex(c)[2:] for c in text.encode()) + ' ')
                self._receive_in_hex = checked
        else:
            if checked != self._receive_in_hex:
                text = self.receive_data_plain_edit.toPlainText().strip()
                self._receive_in_hex = checked
                try:
                    self.receive_data_plain_edit.setPlainText(bytes.fromhex(text).decode('utf-8'))
                except UnicodeDecodeError:
                    try:
                        self.receive_data_plain_edit.setPlainText(bytes.fromhex(text).decode('gbk'))
                    except UnicodeDecodeError:
                        self.receive_data_plain_edit.setPlainText(repr(bytes.fromhex(text)))

    def _open_connection_status(self, status: bool) -> None:
        self.connect_config_combo_box.setEnabled(status)
        self.soft_status.connect_status_text.setText("未连接" if status else "已连接")
        self.single_send_button.setEnabled(not status)

    def _open_serial_port(self) -> None:
        def set_enable(status: bool) -> None:
            self.serial_config.ports_select.setEnabled(status)
            self.serial_config.rate_select.setEnabled(status)
            self.serial_config.data_bits_select.setEnabled(status)
            self.serial_config.verification_select.setEnabled(status)
            self.serial_config.stop_bits_select.setEnabled(status)

        def serial_receive_data_handler() -> None:
            while True:
                sleep(0.01)
                if self._serial_read_data_thread_alive.is_set():
                    break
                if self._serial is None:
                    continue
                size = self._serial.waiting
                if size is None:
                    self._open_serial_port()
                    return
                byte = self._serial.read(size)
                self._receive_data(byte, size)

        if self._serial is None:
            port = self.serial_config.ports_select.currentText()
            rate = self.serial_config.rate_select.currentText()
            if not port:
                return
            data_bits = EIGHTBITS
            match self.serial_config.data_bits_select.currentText():
                case 8:
                    data_bits = EIGHTBITS
                case 7:
                    data_bits = SEVENBITS
                case 6:
                    data_bits = SIXBITS
            verification = PARITY_NONE
            match self.serial_config.verification_select.currentText():
                case "无":
                    verification = PARITY_NONE
                case "奇校验":
                    verification = PARITY_ODD
                case "偶校验":
                    verification = PARITY_EVEN
            stop_bits = STOPBITS_ONE
            match self.serial_config.stop_bits_select.currentText():
                case 1:
                    stop_bits = STOPBITS_ONE
                case 2:
                    stop_bits = STOPBITS_TWO
            set_enable(False)
            self.open_connection_button.setText("关闭串口")
            self._serial = SerialManager(port, rate, data_bits, verification, stop_bits)
            self._serial_read_data_thread_alive.clear()
            self._serial_read_data_thread = thread_pool.submit(
                Thread(target=serial_receive_data_handler, name="SerialReceiveThread", daemon=True).start)
            self._open_connection_status(False)
            return
        set_enable(True)
        self._serial_read_data_thread_alive.set()
        self.open_connection_button.setText("打开串口")
        self._open_connection_status(True)
        self._serial_read_data_thread = None
        self._serial = None

    def _open_udp_connect(self):
        def handler(data, _=None):
            self._receive_data(data, len(data))

        udp = UDPClient(UDPClient.IPProtocol.IPV4, read_handler=handler)
        print(udp)

    def _open_tcp_connect(self):
        def handler(data, _=None):
            self._receive_data(data, len(data))

        tcp = TCPClient(TCPClient.IPProtocol.IPV4, read_handler=handler)
        print(tcp)

    def open_connection(self) -> None:
        match self.connect_config_combo_box.currentIndex():
            case 0:
                self._open_serial_port()
            case 1:
                self._open_udp_connect()
            case 2:
                self._open_tcp_connect()

    @property
    def show_in_hex(self):
        return self.show_in_hex_check_box.isChecked()

    @property
    def single_send_in_hex(self):
        return self.single_send_in_hex_check_box.isChecked()

    @property
    def gbk_encoding(self):
        return self.encoding_in_gbk_check_box.isChecked()

    @property
    def clear_after_send(self):
        return self.clear_after_send_check_box.isChecked()

    @property
    def show_back(self):
        return self.show_back_check_box.isChecked()

    @property
    def send_back(self):
        return self.auto_send_back_check_box.isChecked()

    @property
    def send_new_line(self):
        return self.send_new_line_check_box.isChecked()

    @property
    def save_to_file(self):
        return self.save_to_file_check_box.isChecked()
