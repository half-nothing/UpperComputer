# Form implementation generated from reading ui file 'udp_config_widget.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_UDPConfigWidget(object):
    def setupUi(self, UDPConfigWidget):
        UDPConfigWidget.setObjectName("UDPConfigWidget")
        UDPConfigWidget.resize(200, 120)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UDPConfigWidget.sizePolicy().hasHeightForWidth())
        UDPConfigWidget.setSizePolicy(sizePolicy)
        UDPConfigWidget.setMinimumSize(QtCore.QSize(200, 120))
        UDPConfigWidget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.formLayout = QtWidgets.QFormLayout(UDPConfigWidget)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.formLayout.setContentsMargins(4, 4, 4, 4)
        self.formLayout.setObjectName("formLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.LocalPort = QtWidgets.QLineEdit(parent=UDPConfigWidget)
        self.LocalPort.setObjectName("LocalPort")
        self.gridLayout.addWidget(self.LocalPort, 2, 1, 1, 1)
        self.Connect = QtWidgets.QPushButton(parent=UDPConfigWidget)
        self.Connect.setObjectName("Connect")
        self.gridLayout.addWidget(self.Connect, 3, 0, 1, 2)
        self.RomtePort = QtWidgets.QLineEdit(parent=UDPConfigWidget)
        self.RomtePort.setObjectName("RomtePort")
        self.gridLayout.addWidget(self.RomtePort, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=UDPConfigWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=UDPConfigWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=UDPConfigWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.RomteIp = QtWidgets.QLineEdit(parent=UDPConfigWidget)
        self.RomteIp.setObjectName("RomteIp")
        self.gridLayout.addWidget(self.RomteIp, 0, 1, 1, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.gridLayout)

        self.retranslateUi(UDPConfigWidget)
        QtCore.QMetaObject.connectSlotsByName(UDPConfigWidget)

    def retranslateUi(self, UDPConfigWidget):
        _translate = QtCore.QCoreApplication.translate
        UDPConfigWidget.setWindowTitle(_translate("UDPConfigWidget", "Form"))
        self.LocalPort.setText(_translate("UDPConfigWidget", "8080"))
        self.Connect.setText(_translate("UDPConfigWidget", "连接"))
        self.RomtePort.setText(_translate("UDPConfigWidget", "8080"))
        self.label_3.setText(_translate("UDPConfigWidget", "本地端口"))
        self.label_2.setText(_translate("UDPConfigWidget", "远程端口"))
        self.label.setText(_translate("UDPConfigWidget", "远程IP"))
        self.RomteIp.setText(_translate("UDPConfigWidget", "192.168.1.1"))
