from PyQt6.QtWidgets import QWidget

from form.generate.image_display import Ui_ImageDisplay


class ImageDisplay(QWidget, Ui_ImageDisplay):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
