from binascii import hexlify
from concurrent.futures import Future
from os.path import join
from threading import Event, Thread
from time import sleep
from typing import BinaryIO, Optional, Union

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QImage, QPainter, QPen, QPixmap, QPolygonF, QTextCursor
from PyQt6.QtWidgets import QFileDialog, QMainWindow

from form.generate.main_window import Ui_MainWindow
from module.sockets.tcp_client import TCPClient
from module.sockets.tcp_server import TCPServer
from module.sockets.udp_client import UDPClient
from module.sockets.udp_server import UDPServer
from module.utils.logger import Logger
from module.utils.message_box import show_error_box, show_warn_box
from module.utils.serial_manager import SerialManager
from module.utils.thread_pool_manager import thread_pool


class MainWindow(QMainWindow, Ui_MainWindow):
    _logger: Logger = Logger("MainWindow")
    _receive_in_hex: bool = False
    _send_in_hex: bool = False
    _items: tuple[str] = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' ')
    _serial: Optional[SerialManager] = None
    _serial_read_data_thread: Optional[Future] = None
    _serial_read_data_thread_alive: Event = Event()
    _save_file: Optional[BinaryIO] = None
    _udp_socket: Optional[Union[UDPClient, UDPServer]] = None
    _tcp_socket: Optional[Union[TCPClient, TCPServer]] = None
    _start_marker: bytes = b"\x48\x41\x4C\x46"
    _end_marker: bytes = b"\x46\x4C\x41\x48"
    _line_marker: bytes = b"\x48\x41\x41\x48"
    _global_color: list[Qt.GlobalColor] = [Qt.GlobalColor.red, Qt.GlobalColor.green, Qt.GlobalColor.blue]
    _lines: list[QPolygonF] = []
    _line_number: int = 0
    _images_video: list[QPixmap] = []
    _max_frame: int = 10000
    _auto_save_image_dir: Optional[str] = None
    _total_save_number: int = 0
    _receive_raw_data: bytes = b""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.update_clear_button(self.main_area_widget.currentIndex())

    def save_data_to_file(self, status: bool):
        if status:
            file_path, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "",
                                                       "文本文件(*.txt);;二进制文件(*.dat;*.data;*.bin);;所有文件 (*.*)")
            if file_path:
                self.file_path_edit.setEnabled(True)
                self.file_path_edit.setText(file_path)
                self._save_file = open(file_path, "wb+")
            else:
                self.save_to_file_check_box.setChecked(False)
            return
        self.file_path_edit.setEnabled(False)
        self.file_path_edit.clear()
        self._save_file.close()
        self._save_file = None

    def _receive_data(self, raw_data: bytes, size: int) -> None:
        def mono_decode(mono_data: bytes) -> bytes:
            res_data = b""
            binary_sequence = bin(int(hexlify(mono_data), 16))[2:]
            for i in range(len(binary_sequence)):
                res_data += b"\xFF" if binary_sequence[i] == "1" else b"\x00"
            return res_data

        if not raw_data:
            return
        self.soft_status.total_receive_change_signal.emit(size)
        if self.save_to_file:
            self._save_file.write(raw_data)
            self._save_file.flush()
        match self.main_area_widget.currentIndex():
            case 0:
                if self.send_back:
                    self._serial.send(raw_data)
                if self.show_in_hex:
                    raw_data = ' '.join(hex(c)[2:] for c in raw_data) + ' '
                else:
                    try:
                        raw_data = raw_data.decode("utf-8")
                    except UnicodeDecodeError:
                        try:
                            raw_data = raw_data.decode("gbk")
                        except UnicodeDecodeError:
                            raw_data = repr(raw_data).lstrip('b').strip('\'').replace("\\x", "")
                            raw_data = ' '.join(raw_data[i:i + 2] for i in range(0, len(raw_data), 2)) + ' '
                self.receive_data_plain_edit.insertPlainText(raw_data)
            case 1:
                self._receive_raw_data += raw_data
                start = self._receive_raw_data.find(self._start_marker)
                end = self._receive_raw_data.find(self._end_marker)
                if start == -1 or end == -1:
                    return
                data = self._receive_raw_data[start + len(self._start_marker): end]
                self._receive_raw_data = self._receive_raw_data[end + len(self._end_marker):]
                length = self.image_display.image_size
                real_format = QImage.Format.Format_Indexed8
                line_data: bytes = b""
                if self._line_number:
                    line_marker = data.find(self._line_marker)
                    if line_marker == -1:
                        self._logger.error(f"Can't find line marker")
                        return
                    line_data = data[line_marker + len(self._line_marker):]
                    if len(line_data) != self.image_display.image_height * self._line_number:
                        self._logger.error(f"Line data length error")
                        return
                    data = data[:line_marker]
                if self.image_type == QImage.Format.Format_Mono:
                    length = round(length / 8)
                if self.image_type == QImage.Format.Format_RGB888:
                    real_format = QImage.Format.Format_RGB888
                    length *= 3
                if len(data) != length:
                    self._logger.error(f"{len(data)} don't match image size {length}")
                    return
                if self.image_type == QImage.Format.Format_Mono:
                    data = mono_decode(data)
                image = QImage(data, self.image_display.image_width, self.image_display.image_height,
                               real_format).convertToFormat(QImage.Format.Format_RGB888)
                if self._line_number:
                    paint = QPainter(image)
                    for i in range(self._line_number):
                        if len(self._lines) > i:
                            self._lines[i].clear()
                        else:
                            self._lines.append(QPolygonF())
                        for j in range(self.image_display.image_height):
                            self._lines[i].append(QPointF(int(line_data[j]), j))
                    for i in range(self._line_number):
                        paint.setPen(QPen(self._global_color[i], 1))
                        paint.drawPoints(self._lines[i])
                    paint.end()
                self._images_video.append(QPixmap.fromImage(image))
                size = len(self._images_video)
                if size > self._max_frame:
                    size -= 1
                    del self._images_video[0]
                if self.auto_save_images:
                    self._images_video[size - 1].save(
                        join(self._auto_save_image_dir, f"image{self._total_save_number}.bmp"))
                self.image_slider.setMaximum(size)
                self.image_slider.setValue(size)
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

    def update_config_window(self, index: int) -> None:
        match index:
            case 0:
                self.open_connection_button.setText("打开串口")
            case 1 | 2:
                self.open_connection_button.setText("打开连接")

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
        if self.clear_after_send:
            self.single_send_text_plain_edit.clear()
        match (self.connect_config_widget.currentIndex()):
            case 0:
                self._serial.send(data)
            case 1:
                if self._udp_socket.is_client:
                    self._udp_socket.send_data_to(data)
                else:
                    if self.udp_config.select_addr:
                        self._udp_socket.send_data_to(data, self.udp_config.select_addr)
                    else:
                        show_warn_box("警告", "未选择发送地址")
            case 2:
                if self._tcp_socket.is_client:
                    self._tcp_socket.send_data(data)
                else:
                    if self.tcp_config.select_addr:
                        self._tcp_socket.send_data_to(data, self.tcp_config.select_addr)
                    else:
                        show_warn_box("警告", "未选择发送地址")
        self.soft_status.total_send_change_signal.emit(length)

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
        self.soft_status.connect_status_text.setText("未连接" if status else "已连接")
        self.single_send_button.setEnabled(not status)
        index = self.connect_config_widget.currentIndex()
        for i in range((self.connect_config_widget.count())):
            if i == index:
                continue
            self.connect_config_widget.setTabEnabled(i, status)

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
            port = self.serial_config.connect_port
            rate = self.serial_config.rate
            if not port:
                return
            data_bits = self.serial_config.data_bit
            verification = self.serial_config.verification
            stop_bits = self.serial_config.stop_bit
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
        def set_enable(status: bool) -> None:
            self.udp_config.remote_ip_edit.setEnabled(status)
            self.udp_config.remote_port_edit.setEnabled(status)
            self.udp_config.local_port_edit.setEnabled(status)
            self.udp_config.client_mode_button.setEnabled(status)
            self.udp_config.server_mode_button.setEnabled(status)
            self.udp_config.broadcast_mode_check_box.setEnabled(status)

        def client_handler(data: bytes, _: Optional[tuple[str, int]] = None) -> None:
            self._receive_data(data, len(data))

        def server_handler(data: bytes, addr: tuple[str, int]) -> None:
            self._receive_data(data, len(data))
            self.udp_config.add_item(addr[0], addr[1])

        if self._udp_socket:
            self._udp_socket.clear()
            self._udp_socket = None
            self.open_connection_button.setText("打开连接")
            set_enable(True)
            self._open_connection_status(True)
            return
        if self.udp_config.is_client:
            self._udp_socket = UDPClient(UDPClient.IPProtocol.IPV4, read_handler=client_handler,
                                         remote_host=self.udp_config.remote_host,
                                         remote_port=self.udp_config.remote_port,
                                         local_port=self.udp_config.local_port,
                                         read_buffer=50000)
            self.open_connection_button.setText("关闭连接")
            set_enable(False)
            self._open_connection_status(False)
            return
        self._udp_socket = UDPServer(UDPServer.IPProtocol.IPV4, read_handler=server_handler,
                                     local_host=self.udp_config.remote_host, local_port=self.udp_config.remote_port,
                                     read_buffer=50000)
        self.open_connection_button.setText("关闭连接")
        set_enable(False)
        self._open_connection_status(False)

    def _open_tcp_connect(self):
        def set_enable(status: bool) -> None:
            self.tcp_config.remote_ip_edit.setEnabled(status)
            self.tcp_config.remote_port_edit.setEnabled(status)
            self.tcp_config.local_port_edit.setEnabled(status)
            self.tcp_config.client_mode_button.setEnabled(status)
            self.tcp_config.server_mode_button.setEnabled(status)

        def client_handler(data: bytes) -> None:
            self._receive_data(data, len(data))

        def server_handler(data: bytes, addr: tuple[str, int]) -> None:
            self._receive_data(data, len(data))
            self.tcp_config.add_item(addr[0], addr[1])

        def connect_handler(addr: tuple[str, int]) -> None:
            self.tcp_config.add_item(addr[0], addr[1])

        def disconnect_handler(addr: tuple[str, int]) -> None:
            self.tcp_config.del_item(addr[0], addr[1])

        if self._tcp_socket:
            self._tcp_socket.clear()
            self._tcp_socket = None
            self.open_connection_button.setText("打开连接")
            set_enable(True)
            self._open_connection_status(True)
            return
        if self.tcp_config.is_client:
            try:
                self._tcp_socket = TCPClient(TCPClient.IPProtocol.IPV4, read_handler=client_handler,
                                             remote_host=self.tcp_config.remote_host,
                                             remote_port=self.tcp_config.remote_port,
                                             local_port=self.tcp_config.local_port,
                                             read_buffer=50000)
            except ConnectionError as e:
                show_error_box("发生错误", f"无法连接到远程服务器{e}")
                self._tcp_socket = None
                return
            self.open_connection_button.setText("关闭连接")
            set_enable(False)
            self._open_connection_status(False)
            return
        self._tcp_socket = TCPServer(TCPServer.IPProtocol.IPV4, read_handler=server_handler,
                                     connect_handler=connect_handler, disconnect_handler=disconnect_handler,
                                     local_host=self.tcp_config.remote_host, local_port=self.tcp_config.remote_port,
                                     read_buffer=50000)
        self.open_connection_button.setText("关闭连接")
        set_enable(False)
        self._open_connection_status(False)

    def open_connection(self) -> None:
        match self.connect_config_widget.currentIndex():
            case 0:
                self._open_serial_port()
            case 1:
                self._open_udp_connect()
            case 2:
                self._open_tcp_connect()

    def line_number_change(self, num: str) -> None:
        if num == "":
            return
        self._line_number = int(num)

    def display_select_image(self, value: int) -> None:
        if len(self._images_video) == 0:
            return
        self.image_display.display_image(self._images_video[value - 1])

    def save_all_image(self):
        if len(self._images_video) == 0:
            return
        file_path = QFileDialog.getExistingDirectory(self, "选择保存位置", "")
        if file_path is None:
            return
        for i in range(len(self._images_video)):
            self._images_video[i].save(join(file_path, f"image{i}.bmp"))

    def save_select_image(self):
        if len(self._images_video) == 0:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "",
                                                   "JPEG文件(*.jpg);;PNG文件(*.png);;位图文件(*.bmp)")
        if file_path is None:
            return
        self._images_video[self.image_slider.value() - 1].save(file_path)

    def delete_all_image(self):
        self._images_video.clear()
        self.image_slider.setValue(0)
        self.image_slider.setMaximum(0)

    def delete_select_image(self):
        if len(self._images_video) == 0:
            return
        del self._images_video[self.image_slider.value() - 1]
        length = len(self._images_video)
        self.image_slider.setValue(length - 1)
        self.image_slider.setMaximum(length - 1)

    def auto_save_image(self, value: bool):
        if value:
            file_path = QFileDialog.getExistingDirectory(self, "选择保存位置", "")
            if file_path is None:
                self.auto_save_file_check_box.setChecked(False)
                return
            self._auto_save_image_dir = file_path
            self.image_save_path_edit.setEnabled(True)
            self.image_save_path_edit.setText(file_path)
            return
        self.image_save_path_edit.clear()
        self.image_save_path_edit.setEnabled(False)

    def reset_data(self):
        self._total_save_number = 0
        self._receive_raw_data = b""

    @property
    def auto_save_images(self) -> bool:
        return self.auto_save_file_check_box.isChecked()

    @property
    def show_in_hex(self) -> bool:
        return self.show_in_hex_check_box.isChecked()

    @property
    def single_send_in_hex(self) -> bool:
        return self.single_send_in_hex_check_box.isChecked()

    @property
    def gbk_encoding(self) -> bool:
        return self.encoding_in_gbk_check_box.isChecked()

    @property
    def clear_after_send(self) -> bool:
        return self.clear_after_send_check_box.isChecked()

    @property
    def show_back(self) -> bool:
        return self.show_back_check_box.isChecked()

    @property
    def send_back(self) -> bool:
        return self.auto_send_back_check_box.isChecked()

    @property
    def send_new_line(self) -> bool:
        return self.send_new_line_check_box.isChecked()

    @property
    def save_to_file(self) -> bool:
        return self.save_to_file_check_box.isChecked()

    @property
    def image_type(self) -> QImage.Format:
        match self.image_type_combo_box.currentIndex():
            case 0:
                return QImage.Format.Format_Mono
            case 1:
                return QImage.Format.Format_Indexed8
            case 2:
                return QImage.Format.Format_RGB888
