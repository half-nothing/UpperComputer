# Form implementation generated from reading ui file 'tcp_config_widget.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TCPConfigWidget(object):
    def setupUi(self, TCPConfigWidget):
        TCPConfigWidget.setObjectName("TCPConfigWidget")
        TCPConfigWidget.resize(200, 120)
        TCPConfigWidget.setMinimumSize(QtCore.QSize(200, 120))
        self.formLayout = QtWidgets.QFormLayout(TCPConfigWidget)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.formLayout.setContentsMargins(4, 4, 4, 4)
        self.formLayout.setObjectName("formLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.LocalPort = QtWidgets.QLineEdit(parent=TCPConfigWidget)
        self.LocalPort.setObjectName("LocalPort")
        self.gridLayout.addWidget(self.LocalPort, 2, 1, 1, 1)
        self.Connect = QtWidgets.QPushButton(parent=TCPConfigWidget)
        self.Connect.setObjectName("Connect")
        self.gridLayout.addWidget(self.Connect, 3, 0, 1, 2)
        self.RomtePort = QtWidgets.QLineEdit(parent=TCPConfigWidget)
        self.RomtePort.setObjectName("RomtePort")
        self.gridLayout.addWidget(self.RomtePort, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=TCPConfigWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=TCPConfigWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=TCPConfigWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.RomteIp = QtWidgets.QLineEdit(parent=TCPConfigWidget)
        self.RomteIp.setObjectName("RomteIp")
        self.gridLayout.addWidget(self.RomteIp, 0, 1, 1, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.gridLayout)

        self.retranslateUi(TCPConfigWidget)
        QtCore.QMetaObject.connectSlotsByName(TCPConfigWidget)

    def retranslateUi(self, TCPConfigWidget):
        _translate = QtCore.QCoreApplication.translate
        TCPConfigWidget.setWindowTitle(_translate("TCPConfigWidget", "Form"))
        self.LocalPort.setText(_translate("TCPConfigWidget", "8080"))
        self.Connect.setText(_translate("TCPConfigWidget", "连接"))
        self.RomtePort.setText(_translate("TCPConfigWidget", "8080"))
        self.label_3.setText(_translate("TCPConfigWidget", "本地端口"))
        self.label_2.setText(_translate("TCPConfigWidget", "远程端口"))
        self.label.setText(_translate("TCPConfigWidget", "远程IP"))
        self.RomteIp.setText(_translate("TCPConfigWidget", "192.168.1.1"))
