from PyQt6.QtWidgets import QWidget

from form.generate.tcp_config_widget import Ui_TCPConfigWidget


class TCPConfigWidget(QWidget, Ui_TCPConfigWidget):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
