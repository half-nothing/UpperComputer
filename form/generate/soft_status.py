# Form implementation generated from reading ui file 'soft_status.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_SoftStatus(object):
    def setupUi(self, SoftStatus):
        SoftStatus.setObjectName("SoftStatus")
        SoftStatus.resize(658, 33)
        self.gridLayout = QtWidgets.QGridLayout(SoftStatus)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(parent=SoftStatus)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=SoftStatus)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(parent=SoftStatus)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=SoftStatus)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=SoftStatus)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)

        self.retranslateUi(SoftStatus)
        QtCore.QMetaObject.connectSlotsByName(SoftStatus)

    def retranslateUi(self, SoftStatus):
        _translate = QtCore.QCoreApplication.translate
        SoftStatus.setWindowTitle(_translate("SoftStatus", "Form"))
        self.label_3.setText(_translate("SoftStatus", "已接收字节:"))
        self.label_4.setText(_translate("SoftStatus", "发送速度:"))
        self.label.setText(_translate("SoftStatus", "连接状态："))
        self.label_2.setText(_translate("SoftStatus", "已发送字节:"))
        self.label_5.setText(_translate("SoftStatus", "接受速度:"))