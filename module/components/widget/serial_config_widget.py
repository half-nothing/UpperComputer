from threading import Event, Thread
from time import sleep
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
from serial.serialutil import EIGHTBITS, SEVENBITS, SIXBITS
from serial.serialutil import PARITY_EVEN, PARITY_NONE, PARITY_ODD
from serial.serialutil import STOPBITS_ONE, STOPBITS_TWO

from form.generate.serial_config_widget import Ui_SerialConfigWidget
from module.enums.logger.log_level import LogLevel
from module.utils.logger import Logger
from module.utils.serial_manager import SerialManager


class SerialConfigWidget(QWidget, Ui_SerialConfigWidget):
    _serial: Optional[SerialManager] = None
    _logger: Logger = Logger("SerialWidget", log_level=LogLevel.DEBUG)
    data_changed = pyqtSignal(str, int)
    clear_receive_data_signal = pyqtSignal()
    _ports: set = set()
    _read_data: Event = Event()
    _running: Event = Event()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        Thread(target=self._receive_data_handler, name="Serial_Receive_Data", daemon=True).start()
        self._serial_search_port()

    @property
    def serial(self) -> SerialManager:
        return self._serial

    @serial.setter
    def serial(self, serial) -> None:
        if self._serial is None:
            self._serial = serial
            return
        if self._serial.open:
            self._serial.close()
            self._serial = serial

    def _receive_data_handler(self):
        while True:
            sleep(0.01)
            self._serial_search_port()
            if self._running.is_set():
                break
            if self._read_data.is_set():
                continue
            if self._serial is None:
                continue
            size = self._serial.waiting
            if size is None:
                self._serial_port_option()
                return
            byte = self._serial.read(size)
            self.data_changed.emit(byte.decode("utf-8"), size)

    def _clear_receive_data(self):
        self.clear_receive_data_signal.emit()

    def _serial_port_option(self) -> None:
        if self.serial is None:
            self.ports_select.setEnabled(False)
            self.rate_select.setEnabled(False)
            self.data_bits_select.setEnabled(False)
            self.verification_select.setEnabled(False)
            self.stop_bits_select.setEnabled(False)
            self.open_port_button.setText("关闭串口")
            port = self.ports_select.currentText()
            rate = self.rate_select.currentText()
            data_bits = EIGHTBITS
            match self.data_bits_select.currentText():
                case 8:
                    data_bits = EIGHTBITS
                case 7:
                    data_bits = SEVENBITS
                case 6:
                    data_bits = SIXBITS
            verification = PARITY_NONE
            match self.verification_select.currentText():
                case "无":
                    verification = PARITY_NONE
                case "奇校验":
                    verification = PARITY_ODD
                case "偶校验":
                    verification = PARITY_EVEN
            stop_bits = STOPBITS_ONE
            match self.stop_bits_select.currentText():
                case 1:
                    stop_bits = STOPBITS_ONE
                case 2:
                    stop_bits = STOPBITS_TWO
            self.serial = SerialManager(port, rate, data_bits, verification, stop_bits, logger=self._logger)
            self._read_data.clear()
            return
        self.ports_select.setEnabled(True)
        self.rate_select.setEnabled(True)
        self.data_bits_select.setEnabled(True)
        self.verification_select.setEnabled(True)
        self.stop_bits_select.setEnabled(True)
        self.open_port_button.setText("打开串口")
        self._read_data.set()
        self.serial = None

    def _serial_search_port(self):
        ports = sorted(SerialManager.get_serials())
        ports_set = set(ports)
        if self._ports == ports_set:
            return
        diff = self._ports.difference(ports_set)
        if self.ports_select.currentText() in diff:
            self.ports_select.setCurrentIndex(-1)
        self.ports_select.clear()
        for item in ports:
            self.ports_select.addItem(item)
        self._ports = ports_set
