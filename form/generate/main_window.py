# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 758)
        MainWindow.setMinimumSize(QtCore.QSize(1090, 758))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(686, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.soft_status_box = QtWidgets.QGroupBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.soft_status_box.sizePolicy().hasHeightForWidth())
        self.soft_status_box.setSizePolicy(sizePolicy)
        self.soft_status_box.setMinimumSize(QtCore.QSize(0, 61))
        self.soft_status_box.setObjectName("soft_status_box")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.soft_status_box)
        self.gridLayout_2.setContentsMargins(4, 0, 4, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.soft_status = SoftStatus(parent=self.soft_status_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.soft_status.sizePolicy().hasHeightForWidth())
        self.soft_status.setSizePolicy(sizePolicy)
        self.soft_status.setMinimumSize(QtCore.QSize(0, 33))
        self.soft_status.setObjectName("soft_status")
        self.gridLayout_2.addWidget(self.soft_status, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.soft_status_box, 1, 0, 1, 2)
        self.data_connect_box = QtWidgets.QGroupBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_connect_box.sizePolicy().hasHeightForWidth())
        self.data_connect_box.setSizePolicy(sizePolicy)
        self.data_connect_box.setObjectName("data_connect_box")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.data_connect_box)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.clear_receive_area_button = QtWidgets.QPushButton(parent=self.data_connect_box)
        self.clear_receive_area_button.setEnabled(True)
        self.clear_receive_area_button.setObjectName("clear_receive_area_button")
        self.gridLayout_5.addWidget(self.clear_receive_area_button, 16, 0, 1, 1)
        self.save_to_file_check_box = QtWidgets.QCheckBox(parent=self.data_connect_box)
        self.save_to_file_check_box.setObjectName("save_to_file_check_box")
        self.gridLayout_5.addWidget(self.save_to_file_check_box, 13, 0, 1, 1)
        self.connect_config_box = QtWidgets.QGroupBox(parent=self.data_connect_box)
        self.connect_config_box.setObjectName("connect_config_box")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.connect_config_box)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.connect_config_stack_widget = QtWidgets.QStackedWidget(parent=self.connect_config_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_config_stack_widget.sizePolicy().hasHeightForWidth())
        self.connect_config_stack_widget.setSizePolicy(sizePolicy)
        self.connect_config_stack_widget.setMinimumSize(QtCore.QSize(200, 0))
        self.connect_config_stack_widget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.connect_config_stack_widget.setObjectName("connect_config_stack_widget")
        self.serial_config = SerialConfigWidget()
        self.serial_config.setObjectName("serial_config")
        self.connect_config_stack_widget.addWidget(self.serial_config)
        self.udp_config = UDPConfigWidget()
        self.udp_config.setObjectName("udp_config")
        self.connect_config_stack_widget.addWidget(self.udp_config)
        self.tcp_config = TCPConfigWidget()
        self.tcp_config.setObjectName("tcp_config")
        self.connect_config_stack_widget.addWidget(self.tcp_config)
        self.gridLayout_8.addWidget(self.connect_config_stack_widget, 1, 0, 1, 1)
        self.config_type_layout = QtWidgets.QGridLayout()
        self.config_type_layout.setObjectName("config_type_layout")
        self.connect_config_label = QtWidgets.QLabel(parent=self.connect_config_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_config_label.sizePolicy().hasHeightForWidth())
        self.connect_config_label.setSizePolicy(sizePolicy)
        self.connect_config_label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.connect_config_label.setFont(font)
        self.connect_config_label.setText("连接类型:")
        self.connect_config_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.connect_config_label.setObjectName("connect_config_label")
        self.config_type_layout.addWidget(self.connect_config_label, 0, 0, 1, 1)
        self.connect_config_combo_box = QtWidgets.QComboBox(parent=self.connect_config_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_config_combo_box.sizePolicy().hasHeightForWidth())
        self.connect_config_combo_box.setSizePolicy(sizePolicy)
        self.connect_config_combo_box.setMinimumSize(QtCore.QSize(0, 20))
        self.connect_config_combo_box.setPlaceholderText("")
        self.connect_config_combo_box.setObjectName("connect_config_combo_box")
        self.connect_config_combo_box.addItem("")
        self.connect_config_combo_box.addItem("")
        self.connect_config_combo_box.addItem("")
        self.config_type_layout.addWidget(self.connect_config_combo_box, 0, 1, 1, 1)
        self.gridLayout_8.addLayout(self.config_type_layout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.connect_config_box, 0, 0, 2, 1)
        self.file_path_edit = QtWidgets.QLineEdit(parent=self.data_connect_box)
        self.file_path_edit.setEnabled(False)
        self.file_path_edit.setObjectName("file_path_edit")
        self.gridLayout_5.addWidget(self.file_path_edit, 14, 0, 1, 1)
        self.show_in_hex_check_box = QtWidgets.QCheckBox(parent=self.data_connect_box)
        self.show_in_hex_check_box.setObjectName("show_in_hex_check_box")
        self.gridLayout_5.addWidget(self.show_in_hex_check_box, 4, 0, 1, 1)
        self.show_back_check_box = QtWidgets.QCheckBox(parent=self.data_connect_box)
        self.show_back_check_box.setObjectName("show_back_check_box")
        self.gridLayout_5.addWidget(self.show_back_check_box, 10, 0, 1, 1)
        self.auto_send_back_check_box = QtWidgets.QCheckBox(parent=self.data_connect_box)
        self.auto_send_back_check_box.setObjectName("auto_send_back_check_box")
        self.gridLayout_5.addWidget(self.auto_send_back_check_box, 11, 0, 1, 1)
        self.clear_after_send_check_box = QtWidgets.QCheckBox(parent=self.data_connect_box)
        self.clear_after_send_check_box.setObjectName("clear_after_send_check_box")
        self.gridLayout_5.addWidget(self.clear_after_send_check_box, 8, 0, 1, 1)
        self.clear_data_button = QtWidgets.QPushButton(parent=self.data_connect_box)
        self.clear_data_button.setObjectName("clear_data_button")
        self.gridLayout_5.addWidget(self.clear_data_button, 17, 0, 1, 1)
        self.send_new_line_check_box = QtWidgets.QCheckBox(parent=self.data_connect_box)
        self.send_new_line_check_box.setObjectName("send_new_line_check_box")
        self.gridLayout_5.addWidget(self.send_new_line_check_box, 12, 0, 1, 1)
        self.open_connection_button = QtWidgets.QPushButton(parent=self.data_connect_box)
        self.open_connection_button.setObjectName("open_connection_button")
        self.gridLayout_5.addWidget(self.open_connection_button, 15, 0, 1, 1)
        self.gridLayout_6.addWidget(self.data_connect_box, 0, 0, 1, 1)
        self.main_area_widget = QtWidgets.QTabWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_area_widget.sizePolicy().hasHeightForWidth())
        self.main_area_widget.setSizePolicy(sizePolicy)
        self.main_area_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.main_area_widget.setObjectName("main_area_widget")
        self.debug_helper = QtWidgets.QWidget()
        self.debug_helper.setObjectName("debug_helper")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.debug_helper)
        self.verticalLayout.setObjectName("verticalLayout")
        self.receive_data_box = QtWidgets.QGroupBox(parent=self.debug_helper)
        self.receive_data_box.setObjectName("receive_data_box")
        self.gridLayout = QtWidgets.QGridLayout(self.receive_data_box)
        self.gridLayout.setObjectName("gridLayout")
        self.receive_data_plain_edit = QtWidgets.QPlainTextEdit(parent=self.receive_data_box)
        self.receive_data_plain_edit.setObjectName("receive_data_plain_edit")
        self.gridLayout.addWidget(self.receive_data_plain_edit, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.receive_data_box)
        self.send_data_box = QtWidgets.QTabWidget(parent=self.debug_helper)
        self.send_data_box.setObjectName("send_data_box")
        self.single_send_layout = QtWidgets.QWidget()
        self.single_send_layout.setObjectName("single_send_layout")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.single_send_layout)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.single_send_in_hex_check_box = QtWidgets.QCheckBox(parent=self.single_send_layout)
        self.single_send_in_hex_check_box.setChecked(False)
        self.single_send_in_hex_check_box.setTristate(False)
        self.single_send_in_hex_check_box.setObjectName("single_send_in_hex_check_box")
        self.gridLayout_7.addWidget(self.single_send_in_hex_check_box, 1, 0, 1, 1)
        self.single_send_button = QtWidgets.QPushButton(parent=self.single_send_layout)
        self.single_send_button.setEnabled(False)
        self.single_send_button.setObjectName("single_send_button")
        self.gridLayout_7.addWidget(self.single_send_button, 1, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_7.addItem(spacerItem, 1, 2, 1, 1)
        self.single_clear_button = QtWidgets.QPushButton(parent=self.single_send_layout)
        self.single_clear_button.setObjectName("single_clear_button")
        self.gridLayout_7.addWidget(self.single_clear_button, 1, 3, 1, 1)
        self.single_send_text_plain_edit = QtWidgets.QPlainTextEdit(parent=self.single_send_layout)
        self.single_send_text_plain_edit.setObjectName("single_send_text_plain_edit")
        self.gridLayout_7.addWidget(self.single_send_text_plain_edit, 0, 0, 1, 6)
        self.encoding_in_gbk_check_box = QtWidgets.QCheckBox(parent=self.single_send_layout)
        self.encoding_in_gbk_check_box.setObjectName("encoding_in_gbk_check_box")
        self.gridLayout_7.addWidget(self.encoding_in_gbk_check_box, 1, 1, 1, 1)
        self.send_data_box.addTab(self.single_send_layout, "")
        self.multiterm_send = QtWidgets.QWidget()
        self.multiterm_send.setObjectName("multiterm_send")
        self.send_data_box.addTab(self.multiterm_send, "")
        self.verticalLayout.addWidget(self.send_data_box)
        self.main_area_widget.addTab(self.debug_helper, "")
        self.camera = QtWidgets.QWidget()
        self.camera.setObjectName("camera")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.camera)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.image_setting_box = QtWidgets.QGroupBox(parent=self.camera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_setting_box.sizePolicy().hasHeightForWidth())
        self.image_setting_box.setSizePolicy(sizePolicy)
        self.image_setting_box.setObjectName("image_setting_box")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.image_setting_box)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.ImageWidthEdit = QtWidgets.QLineEdit(parent=self.image_setting_box)
        self.ImageWidthEdit.setObjectName("ImageWidthEdit")
        self.gridLayout_9.addWidget(self.ImageWidthEdit, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.image_setting_box)
        self.label_2.setObjectName("label_2")
        self.gridLayout_9.addWidget(self.label_2, 0, 0, 1, 1)
        self.ImageType = QtWidgets.QComboBox(parent=self.image_setting_box)
        self.ImageType.setObjectName("ImageType")
        self.ImageType.addItem("")
        self.ImageType.addItem("")
        self.ImageType.addItem("")
        self.gridLayout_9.addWidget(self.ImageType, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.image_setting_box)
        self.label_4.setObjectName("label_4")
        self.gridLayout_9.addWidget(self.label_4, 6, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(parent=self.image_setting_box)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_9.addWidget(self.checkBox, 9, 0, 1, 2)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.image_setting_box)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_9.addWidget(self.pushButton_4, 11, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_9.addItem(spacerItem1, 16, 0, 1, 2)
        self.LineNumberEdit = QtWidgets.QLineEdit(parent=self.image_setting_box)
        self.LineNumberEdit.setObjectName("LineNumberEdit")
        self.gridLayout_9.addWidget(self.LineNumberEdit, 6, 1, 1, 1)
        self.ImageHeightEdit = QtWidgets.QLineEdit(parent=self.image_setting_box)
        self.ImageHeightEdit.setObjectName("ImageHeightEdit")
        self.gridLayout_9.addWidget(self.ImageHeightEdit, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.image_setting_box)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_9.addWidget(self.pushButton_3, 15, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.image_setting_box)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_9.addWidget(self.pushButton_2, 14, 0, 1, 2)
        self.label = QtWidgets.QLabel(parent=self.image_setting_box)
        self.label.setObjectName("label")
        self.gridLayout_9.addWidget(self.label, 2, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.image_setting_box)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_9.addWidget(self.checkBox_2, 8, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(parent=self.image_setting_box)
        self.label_3.setObjectName("label_3")
        self.gridLayout_9.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.image_setting_box)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_9.addWidget(self.lineEdit, 10, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(parent=self.image_setting_box)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_9.addWidget(self.pushButton, 12, 0, 1, 2)
        self.checkBox_3 = QtWidgets.QCheckBox(parent=self.image_setting_box)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_9.addWidget(self.checkBox_3, 7, 0, 1, 2)
        self.gridLayout_3.addWidget(self.image_setting_box, 0, 0, 2, 1)
        self.image_display = ImageDisplay(parent=self.camera)
        self.image_display.setObjectName("image_display")
        self.gridLayout_3.addWidget(self.image_display, 0, 1, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(parent=self.camera)
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_3.addWidget(self.horizontalSlider, 1, 1, 1, 1)
        self.main_area_widget.addTab(self.camera, "")
        self.electromagnetism = QtWidgets.QWidget()
        self.electromagnetism.setObjectName("electromagnetism")
        self.main_area_widget.addTab(self.electromagnetism, "")
        self.gridLayout_6.addWidget(self.main_area_widget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.connect_config_stack_widget.setCurrentIndex(0)
        self.main_area_widget.setCurrentIndex(0)
        self.send_data_box.setCurrentIndex(0)
        self.connect_config_combo_box.currentIndexChanged['int'].connect(MainWindow.update_config_window) # type: ignore
        self.receive_data_plain_edit.textChanged.connect(MainWindow.scroll_to_bottom) # type: ignore
        self.single_clear_button.clicked.connect(self.single_send_text_plain_edit.clear) # type: ignore
        self.main_area_widget.currentChanged['int'].connect(MainWindow.update_clear_button) # type: ignore
        self.single_send_button.clicked.connect(MainWindow.send_data) # type: ignore
        self.single_send_in_hex_check_box.clicked['bool'].connect(MainWindow.send_show_in_hex) # type: ignore
        self.clear_data_button.clicked.connect(self.soft_status.clear) # type: ignore
        self.clear_receive_area_button.clicked.connect(self.receive_data_plain_edit.clear) # type: ignore
        self.open_connection_button.clicked.connect(MainWindow.open_connection) # type: ignore
        self.show_in_hex_check_box.clicked['bool'].connect(MainWindow.receive_show_in_hex) # type: ignore
        self.save_to_file_check_box.clicked['bool'].connect(MainWindow.save_data_to_file) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "上海电机学院上位机"))
        self.soft_status_box.setTitle(_translate("MainWindow", "连接状态"))
        self.data_connect_box.setTitle(_translate("MainWindow", "数据接口"))
        self.clear_receive_area_button.setText(_translate("MainWindow", "清空接收区"))
        self.save_to_file_check_box.setText(_translate("MainWindow", "接受数据到文件"))
        self.connect_config_box.setTitle(_translate("MainWindow", "连接配置"))
        self.connect_config_combo_box.setCurrentText(_translate("MainWindow", "串口"))
        self.connect_config_combo_box.setItemText(0, _translate("MainWindow", "串口"))
        self.connect_config_combo_box.setItemText(1, _translate("MainWindow", "UDP"))
        self.connect_config_combo_box.setItemText(2, _translate("MainWindow", "TCP"))
        self.show_in_hex_check_box.setText(_translate("MainWindow", "16进制显示"))
        self.show_back_check_box.setText(_translate("MainWindow", "回显"))
        self.auto_send_back_check_box.setText(_translate("MainWindow", "接受回发"))
        self.clear_after_send_check_box.setText(_translate("MainWindow", "发送完自动清空"))
        self.clear_data_button.setText(_translate("MainWindow", "清空统计数据"))
        self.send_new_line_check_box.setText(_translate("MainWindow", "发送新行"))
        self.open_connection_button.setText(_translate("MainWindow", "打开串口"))
        self.receive_data_box.setTitle(_translate("MainWindow", "接收区"))
        self.single_send_in_hex_check_box.setText(_translate("MainWindow", "十六进制发送"))
        self.single_send_button.setText(_translate("MainWindow", "发送"))
        self.single_clear_button.setText(_translate("MainWindow", "清空"))
        self.encoding_in_gbk_check_box.setText(_translate("MainWindow", "GBK编码"))
        self.send_data_box.setTabText(self.send_data_box.indexOf(self.single_send_layout), _translate("MainWindow", "单项发送"))
        self.send_data_box.setTabText(self.send_data_box.indexOf(self.multiterm_send), _translate("MainWindow", "多项发送"))
        self.main_area_widget.setTabText(self.main_area_widget.indexOf(self.debug_helper), _translate("MainWindow", "调试助手"))
        self.image_setting_box.setTitle(_translate("MainWindow", "图像设置"))
        self.ImageWidthEdit.setText(_translate("MainWindow", "188"))
        self.label_2.setText(_translate("MainWindow", "图像高度"))
        self.ImageType.setItemText(0, _translate("MainWindow", "二值化"))
        self.ImageType.setItemText(1, _translate("MainWindow", "灰度图"))
        self.ImageType.setItemText(2, _translate("MainWindow", "RGB"))
        self.label_4.setText(_translate("MainWindow", "直线个数"))
        self.checkBox.setText(_translate("MainWindow", "自动保存图片"))
        self.pushButton_4.setText(_translate("MainWindow", "删除当前图片"))
        self.LineNumberEdit.setText(_translate("MainWindow", "0"))
        self.ImageHeightEdit.setText(_translate("MainWindow", "120"))
        self.pushButton_3.setText(_translate("MainWindow", "保存所有图片"))
        self.pushButton_2.setText(_translate("MainWindow", "保存当前图片"))
        self.label.setText(_translate("MainWindow", "图像宽度"))
        self.checkBox_2.setText(_translate("MainWindow", "自动跟踪"))
        self.label_3.setText(_translate("MainWindow", "图像格式"))
        self.pushButton.setText(_translate("MainWindow", "删除所有图片"))
        self.checkBox_3.setText(_translate("MainWindow", "鼠标坐标显示"))
        self.main_area_widget.setTabText(self.main_area_widget.indexOf(self.camera), _translate("MainWindow", "摄像头组"))
        self.main_area_widget.setTabText(self.main_area_widget.indexOf(self.electromagnetism), _translate("MainWindow", "电磁组"))
from module.components.widget.image_display import ImageDisplay
from module.components.widget.serial_config_widget import SerialConfigWidget
from module.components.widget.soft_status import SoftStatus
from module.components.widget.tcp_config_widget import TCPConfigWidget
from module.components.widget.udp_config_widget import UDPConfigWidget
