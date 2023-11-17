from PyQt6.QtWidgets import QMessageBox


def show_warn_box(title: str, content: str) -> int:
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(content)
    msg_box.addButton(QMessageBox.StandardButton.Ok)
    return msg_box.exec()


def show_info_box(title: str, content: str) -> int:
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(content)
    msg_box.addButton(QMessageBox.StandardButton.Ok)
    return msg_box.exec()
