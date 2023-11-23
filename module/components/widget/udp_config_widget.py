from typing import Optional

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QWidget

from form.generate.udp_config_widget import Ui_UDPConfigWidget
from module.sockets.sockets import Sockets


class UDPConfigWidget(QWidget, Ui_UDPConfigWidget):
    _mode: Sockets.SocketMode = Sockets.SocketMode.Client
    model: QStandardItemModel
    select_host: Optional[str] = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = QStandardItemModel(self)
        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(["IP地址", "端口"])
        self.client_show_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.client_show_view.setModel(self.model)

    def add_item(self, host, port):
        row = self.model.rowCount()
        host = QStandardItem(host)
        host.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        port = QStandardItem(str(port))
        port.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.model.setItem(row, 0, host)
        self.model.setItem(row, 1, port)

    def set_select_host(self, value: QModelIndex):
        row = value.row()
        self.select_host = f"{self.model.item(row, 0).text()}:{self.model.item(row, 1).text()}"

    def set_server_mode(self):
        self._mode = Sockets.SocketMode.Server
        self.remote_ip_label.setText("监听地址")
        self.remote_ip_edit.setText("0.0.0.0")
        self.remote_port_label.setText("监听端口")
        self.local_port_label.setEnabled(False)
        self.local_port_edit.setEnabled(False)
        self.set_broadcast_mode(self.broadcast)

    def set_client_mode(self):
        self._mode = Sockets.SocketMode.Client
        self.remote_ip_label.setText("远程地址")
        self.remote_port_label.setText("远程端口")
        self.local_port_label.setEnabled(True)
        self.local_port_edit.setEnabled(True)

    def set_broadcast_mode(self, status: bool):
        if self.is_server:
            if status:
                self.remote_ip_label.setText("广播地址")
                self.remote_ip_edit.setText("255.255.255.255")
                self.remote_port_label.setText("广播端口")
                self.local_port_label.setEnabled(True)
                self.local_port_edit.setEnabled(True)
                return
            self.remote_ip_label.setText("监听地址")
            self.remote_ip_edit.setText("0.0.0.0")
            self.remote_port_label.setText("监听端口")
            self.local_port_label.setEnabled(False)
            self.local_port_edit.setEnabled(False)

    @property
    def broadcast(self):
        return self.broadcast_mode_check_box.isChecked()

    @property
    def remote_host(self):
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
