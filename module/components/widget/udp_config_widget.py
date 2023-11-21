from PyQt6.QtWidgets import QWidget

from form.generate.udp_config_widget import Ui_UDPConfigWidget
from module.sockets.sockets import Sockets


class UDPConfigWidget(QWidget, Ui_UDPConfigWidget):
    _temp_host: str = "192.168.1.1"
    _mode: Sockets.SocketMode = Sockets.SocketMode.Client

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_server_mode(self):
        self._temp_host = self.remote_ip_edit.text()
        self.remote_ip_edit.setText("0.0.0.0")
        self.remote_ip_label.setText("监听地址")
        self.remote_port_label.setText("监听端口")
        self.local_port_edit.setEnabled(False)
        self.local_port_label.setEnabled(False)
        self._mode = Sockets.SocketMode.Server

    def set_client_mode(self):
        self.remote_ip_edit.setText(self._temp_host)
        self.remote_ip_label.setText("远程地址")
        self.remote_port_label.setText("远程端口")
        self.local_port_edit.setEnabled(True)
        self.local_port_label.setEnabled(True)
        self._mode = Sockets.SocketMode.Client

    def set_broadcast_mode(self, status: bool):
        if status:
            self._temp_host = self.remote_ip_edit.text()
            if self._mode == Sockets.SocketMode.Client:
                self.remote_ip_edit.setText("0.0.0.0")
                self.remote_ip_label.setText("监听地址")
                self.remote_port_label.setText("监听端口")
                self.local_port_edit.setEnabled(False)
                self.local_port_label.setEnabled(False)
            else:
                self.remote_ip_edit.setText("255.255.255.255")
                self.remote_ip_label.setText("广播地址")
                self.remote_port_label.setText("广播端口")
                self.local_port_edit.setEnabled(False)
                self.local_port_label.setEnabled(False)
            return
        if self._mode == Sockets.SocketMode.Client:
            self.set_client_mode()
            return
        self.set_server_mode()

    @property
    def broadcast(self):
        return self.broadcast_mode_check_box.isChecked()

    @broadcast.setter
    def broadcast(self, status: bool):
        self.broadcast_mode_check_box.setChecked(status)
