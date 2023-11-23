from threading import Event, Timer

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from form.generate.soft_status import Ui_SoftStatus
from module.utils.thread_pool_manager import thread_pool


class SoftStatus(QWidget, Ui_SoftStatus):
    total_send_change_signal = pyqtSignal(int)
    total_receive_change_signal = pyqtSignal(int)

    _total_send: int = 0
    _send: int = 0
    _total_receive: int = 0
    _receive: int = 0
    _timer: Timer
    _exit: Event = Event()

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.total_send_change_signal.connect(self._send_change)
        self.total_receive_change_signal.connect(self._receive_change)
        self._start_timer()

    def clear(self) -> None:
        self._total_send = 0
        self._total_receive = 0
        self._send = 0
        self._receive = 0
        self.total_send_text.setText(str(self._total_send))
        self.total_receive_text.setText(str(self._total_receive))
        self.send_speed_text.setText(f"{str(self._send)}字节/s")
        self.receive_speed_text.setText(f"{str(self._receive)}字节/s")

    def _start_timer(self) -> None:
        self._timer = Timer(1, self._calculate_speed)
        self._timer.daemon = True
        self._timer.name = "TransformRateTimer"
        thread_pool.submit(self._timer.start)

    def _calculate_speed(self) -> None:
        self.send_speed_text.setText(f"{str(self._send)}字节/s")
        self.receive_speed_text.setText(f"{str(self._receive)}字节/s")
        self._send = 0
        self._receive = 0
        self._start_timer()

    def _send_change(self, change_value: int) -> None:
        self._total_send += change_value
        self._send += change_value
        self.total_send_text.setText(str(self._total_send))

    def _receive_change(self, change_value: int) -> None:
        self._total_receive += change_value
        self._receive += change_value
        self.total_receive_text.setText(str(self._total_receive))
