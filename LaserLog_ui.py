# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\projects\laser_log\LaserLog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1046, 631)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tblLaserLog = QtWidgets.QTableView(self.centralwidget)
        self.tblLaserLog.setMinimumSize(QtCore.QSize(400, 0))
        self.tblLaserLog.setObjectName("tblLaserLog")
        self.verticalLayout.addWidget(self.tblLaserLog)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.tblLaserCond = QtWidgets.QTableView(self.centralwidget)
        self.tblLaserCond.setMinimumSize(QtCore.QSize(400, 0))
        self.tblLaserCond.setObjectName("tblLaserCond")
        self.verticalLayout.addWidget(self.tblLaserCond)
        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(2, 2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(100, 100))
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.pnFilter = QtWidgets.QLineEdit(self.centralwidget)
        self.pnFilter.setMinimumSize(QtCore.QSize(150, 30))
        self.pnFilter.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pnFilter.setObjectName("pnFilter")
        self.verticalLayout_4.addWidget(self.pnFilter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.condFilter = QtWidgets.QLineEdit(self.centralwidget)
        self.condFilter.setMinimumSize(QtCore.QSize(150, 30))
        self.condFilter.setMaximumSize(QtCore.QSize(16777215, 30))
        self.condFilter.setObjectName("condFilter")
        self.verticalLayout_4.addWidget(self.condFilter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem)
        self.btnStartSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartSearch.setMinimumSize(QtCore.QSize(0, 40))
        self.btnStartSearch.setObjectName("btnStartSearch")
        self.verticalLayout_4.addWidget(self.btnStartSearch)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem1)
        self.btnRefreshCache = QtWidgets.QPushButton(self.centralwidget)
        self.btnRefreshCache.setMinimumSize(QtCore.QSize(0, 40))
        self.btnRefreshCache.setObjectName("btnRefreshCache")
        self.verticalLayout_4.addWidget(self.btnRefreshCache)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btnSaveCond = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveCond.setMinimumSize(QtCore.QSize(0, 40))
        self.btnSaveCond.setObjectName("btnSaveCond")
        self.verticalLayout_5.addWidget(self.btnSaveCond)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "三菱镭射机加工记录查询"))
        self.label.setText(_translate("MainWindow", "加工型号筛选："))
        self.label_2.setText(_translate("MainWindow", "镭射参数筛选："))
        self.btnStartSearch.setText(_translate("MainWindow", "搜索加工记录"))
        self.btnRefreshCache.setText(_translate("MainWindow", "刷新本地数据缓存"))
        self.btnSaveCond.setText(_translate("MainWindow", "保存当前镭射参数"))
import icon_rc