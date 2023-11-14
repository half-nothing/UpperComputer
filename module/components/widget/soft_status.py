from PyQt6.QtWidgets import QWidget

from form.generate.soft_status import Ui_SoftStatus


class SoftStatus(QWidget, Ui_SoftStatus):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
