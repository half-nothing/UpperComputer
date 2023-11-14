import sys

from PyQt6.QtWidgets import QApplication

from module.enums.logger.log_level import LogLevel
from module.main_window import MainWindow
from module.utils.logger import Logger

if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    logger = Logger("Main", log_level=LogLevel.DEBUG)
    logger.debug("Logger Test")
    application.show()
    sys.exit(app.exec())
