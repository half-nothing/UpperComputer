from PyQt6.QtWidgets import QWidget

from form.generate.udp_config_widget import Ui_UDPConfigWidget


class UDPConfigWidget(QWidget, Ui_UDPConfigWidget):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
