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
        UDPConfigWidget.resize(200, 386)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UDPConfigWidget.sizePolicy().hasHeightForWidth())
        UDPConfigWidget.setSizePolicy(sizePolicy)
        UDPConfigWidget.setMinimumSize(QtCore.QSize(200, 169))
        UDPConfigWidget.setMaximumSize(QtCore.QSize(2000, 16777215))
        self.gridLayout_2 = QtWidgets.QGridLayout(UDPConfigWidget)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.remote_port_edit = QtWidgets.QLineEdit(parent=UDPConfigWidget)
        self.remote_port_edit.setObjectName("remote_port_edit")
        self.gridLayout.addWidget(self.remote_port_edit, 1, 1, 1, 2)
        self.remote_ip_label = QtWidgets.QLabel(parent=UDPConfigWidget)
        self.remote_ip_label.setObjectName("remote_ip_label")
        self.gridLayout.addWidget(self.remote_ip_label, 0, 0, 1, 1)
        self.client_show_view = QtWidgets.QTableView(parent=UDPConfigWidget)
        self.client_show_view.setEnabled(False)
        self.client_show_view.setMaximumSize(QtCore.QSize(190, 220))
        self.client_show_view.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.client_show_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.client_show_view.setObjectName("client_show_view")
        self.client_show_view.horizontalHeader().setStretchLastSection(False)
        self.client_show_view.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.client_show_view, 6, 0, 1, 3)
        self.remote_port_label = QtWidgets.QLabel(parent=UDPConfigWidget)
        self.remote_port_label.setObjectName("remote_port_label")
        self.gridLayout.addWidget(self.remote_port_label, 1, 0, 1, 1)
        self.client_mode_button = QtWidgets.QRadioButton(parent=UDPConfigWidget)
        self.client_mode_button.setChecked(True)
        self.client_mode_button.setObjectName("client_mode_button")
        self.socket_mode_group = QtWidgets.QButtonGroup(UDPConfigWidget)
        self.socket_mode_group.setObjectName("socket_mode_group")
        self.socket_mode_group.addButton(self.client_mode_button)
        self.gridLayout.addWidget(self.client_mode_button, 3, 0, 1, 3)
        self.broadcast_mode_check_box = QtWidgets.QCheckBox(parent=UDPConfigWidget)
        self.broadcast_mode_check_box.setObjectName("broadcast_mode_check_box")
        self.gridLayout.addWidget(self.broadcast_mode_check_box, 5, 0, 1, 3)
        self.local_port_label = QtWidgets.QLabel(parent=UDPConfigWidget)
        self.local_port_label.setObjectName("local_port_label")
        self.gridLayout.addWidget(self.local_port_label, 2, 0, 1, 1)
        self.remote_ip_edit = QtWidgets.QLineEdit(parent=UDPConfigWidget)
        self.remote_ip_edit.setObjectName("remote_ip_edit")
        self.gridLayout.addWidget(self.remote_ip_edit, 0, 1, 1, 2)
        self.server_mode_button = QtWidgets.QRadioButton(parent=UDPConfigWidget)
        self.server_mode_button.setObjectName("server_mode_button")
        self.socket_mode_group.addButton(self.server_mode_button)
        self.gridLayout.addWidget(self.server_mode_button, 4, 0, 1, 3)
        self.local_port_edit = QtWidgets.QLineEdit(parent=UDPConfigWidget)
        self.local_port_edit.setObjectName("local_port_edit")
        self.gridLayout.addWidget(self.local_port_edit, 2, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(UDPConfigWidget)
        self.server_mode_button.clicked.connect(UDPConfigWidget.set_server_mode) # type: ignore
        self.client_mode_button.clicked.connect(UDPConfigWidget.set_client_mode) # type: ignore
        self.broadcast_mode_check_box.clicked['bool'].connect(UDPConfigWidget.set_broadcast_mode) # type: ignore
        self.client_show_view.clicked['QModelIndex'].connect(UDPConfigWidget.set_select_host) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(UDPConfigWidget)

    def retranslateUi(self, UDPConfigWidget):
        _translate = QtCore.QCoreApplication.translate
        UDPConfigWidget.setWindowTitle(_translate("UDPConfigWidget", "Form"))
        self.remote_port_edit.setText(_translate("UDPConfigWidget", "8080"))
        self.remote_ip_label.setText(_translate("UDPConfigWidget", "远程地址"))
        self.remote_port_label.setText(_translate("UDPConfigWidget", "远程端口"))
        self.client_mode_button.setText(_translate("UDPConfigWidget", "客户端"))
        self.broadcast_mode_check_box.setText(_translate("UDPConfigWidget", "广播模式"))
        self.local_port_label.setText(_translate("UDPConfigWidget", "本地端口"))
        self.remote_ip_edit.setText(_translate("UDPConfigWidget", "192.168.1.1"))
        self.server_mode_button.setText(_translate("UDPConfigWidget", "服务端"))
        self.local_port_edit.setText(_translate("UDPConfigWidget", "8080"))
