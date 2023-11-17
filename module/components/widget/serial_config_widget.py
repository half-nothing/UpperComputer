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
