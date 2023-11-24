from typing import Optional

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QHeaderView, QWidget

from form.generate.tcp_config_widget import Ui_TCPConfigWidget
from module.sockets.sockets import Sockets


class TCPConfigWidget(QWidget, Ui_TCPConfigWidget):
    _mode: Sockets.SocketMode = Sockets.SocketMode.Client
    model: QStandardItemModel
    select_addr: Optional[tuple[str, int]] = None

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.model = QStandardItemModel(self)
        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(["IP地址", "端口"])
        self.client_show_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.client_show_view.setModel(self.model)

    def add_item(self, host, port) -> bool:
        row = self.model.rowCount()
        port = str(port)
        for i in range(row):
            if self.model.item(i, 0).text() == host and self.model.item(i, 1).text() == port:
                return False
        host = QStandardItem(host)
        host.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        port = QStandardItem(port)
        port.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.model.setItem(row, 0, host)
        self.model.setItem(row, 1, port)
        return True

    def del_item(self, host, port) -> bool:
        port = str(port)
        find_list = self.model.findItems(host, Qt.MatchFlag.MatchExactly, 0)
        if not find_list:
            return False
        for item in find_list:
            row = item.row()
            if self.model.item(row, 1).text() == port:
                self.model.removeRow(row)
                return True
        return False

    def set_select_host(self, value: QModelIndex) -> None:
        row = value.row()
        self.select_addr = (self.model.item(row, 0).text(), int(self.model.item(row, 1).text()))

    def set_server_mode(self) -> None:
        self._mode = Sockets.SocketMode.Server
        self.remote_ip_label.setText("监听地址")
        self.remote_ip_edit.setText("0.0.0.0")
        self.remote_port_label.setText("监听端口")
        self.local_port_label.setEnabled(False)
        self.local_port_edit.setEnabled(False)
        self.client_show_view.setEnabled(True)

    def set_client_mode(self) -> None:
        self._mode = Sockets.SocketMode.Client
        self.remote_ip_label.setText("远程地址")
        self.remote_port_label.setText("远程端口")
        self.client_show_view.setEnabled(False)
        self.local_port_label.setEnabled(True)
        self.local_port_edit.setEnabled(True)

    @property
    def remote_host(self) -> str:
        return self.remote_ip_edit.text()

    @property
    def remote_port(self) -> int:
        return int(self.remote_port_edit.text())

    @property
    def local_port(self) -> int:
        return int(self.local_port_edit.text())

    @property
    def mode(self) -> Sockets.SocketMode:
        return self._mode

    @property
    def is_client(self):
        return self._mode == Sockets.SocketMode.Client

    @property
    def is_server(self):
        return self._mode == Sockets.SocketMode.Server
