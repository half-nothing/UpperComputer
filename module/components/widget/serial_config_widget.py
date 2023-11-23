from threading import Timer

from PyQt6.QtWidgets import QWidget

from form.generate.serial_config_widget import Ui_SerialConfigWidget
from module.utils.serial_manager import SerialManager
from module.utils.thread_pool_manager import thread_pool


class SerialConfigWidget(QWidget, Ui_SerialConfigWidget):
    _ports: set = set()
    _timer: Timer

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self._start_timer()

    def _start_timer(self) -> None:
        self._timer = Timer(1, self._serial_search_port)
        self._timer.daemon = True
        self._timer.name = "SerialTimer"
        thread_pool.submit(self._timer.start)

    def _serial_search_port(self) -> None:
        ports = sorted(SerialManager.get_serials())
        if not ports:
            ports.append("无")
        ports_set = set(ports)
        if self._ports == ports_set:
            self._start_timer()
            return
        diff = self._ports.difference(ports_set)
        text = self.ports_select.currentText()
        if text in diff:
            self.ports_select.setCurrentIndex(-1)
        self.ports_select.clear()
        i = 0
        for item in ports:
            if item == text:
                self.ports_select.setCurrentIndex(i)
            i += 1
            self.ports_select.addItem(item)
        self._ports = ports_set
        self._start_timer()

    @property
    def connect_port(self) -> str:
        return self.ports_select.currentText()

    @property
    def rate(self) -> int:
        return self.rate_select.currentText()

    @property
    def data_bit(self) -> SerialManager.ByteSize:
        data_bits = SerialManager.ByteSize.EightBits
        match self.data_bits_select.currentText():
            case 8:
                data_bits = SerialManager.ByteSize.EightBits
            case 7:
                data_bits = SerialManager.ByteSize.SevenBits
            case 6:
                data_bits = SerialManager.ByteSize.SixBits
        return data_bits

    @property
    def stop_bit(self) -> SerialManager.StopBits:
        stop_bits = SerialManager.StopBits.OneBit
        match self.stop_bits_select.currentText():
            case 1:
                stop_bits = SerialManager.StopBits.OneBit
            case 2:
                stop_bits = SerialManager.StopBits.TwoBit
        return stop_bits

    @property
    def verification(self) -> SerialManager.Parity:
        verification = SerialManager.Parity.ParityNone
        match self.verification_select.currentText():
            case "无":
                verification = SerialManager.Parity.ParityNone
            case "奇校验":
                verification = SerialManager.Parity.ParityOdd
            case "偶校验":
                verification = SerialManager.Parity.ParityEven
        return verification
