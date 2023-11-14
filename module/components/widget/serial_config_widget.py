from typing import Optional

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

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.serial_search_port()

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

    def serial_port_option(self) -> None:
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
            return
        self.ports_select.setEnabled(True)
        self.rate_select.setEnabled(True)
        self.data_bits_select.setEnabled(True)
        self.verification_select.setEnabled(True)
        self.stop_bits_select.setEnabled(True)
        self.open_port_button.setText("打开串口")
        self.serial = None

    def serial_search_port(self):
        self.ports_select.clear()
        ports = SerialManager.get_serials()
        self._logger.debug(str(ports))
        for item in ports:
            self.ports_select.addItem(item)
