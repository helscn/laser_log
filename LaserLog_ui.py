# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LaserLog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableView,
    QVBoxLayout, QWidget)
import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1046, 631)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tblLaserLog = QTableView(self.centralwidget)
        self.tblLaserLog.setObjectName(u"tblLaserLog")
        self.tblLaserLog.setMinimumSize(QSize(400, 0))

        self.verticalLayout.addWidget(self.tblLaserLog)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.tblLaserCond = QTableView(self.centralwidget)
        self.tblLaserCond.setObjectName(u"tblLaserCond")
        self.tblLaserCond.setMinimumSize(QSize(400, 0))

        self.verticalLayout.addWidget(self.tblLaserCond)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(2, 3)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(100, 100))

        self.verticalLayout_4.addWidget(self.label)

        self.pnFilter = QLineEdit(self.centralwidget)
        self.pnFilter.setObjectName(u"pnFilter")
        self.pnFilter.setMinimumSize(QSize(150, 30))
        self.pnFilter.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_4.addWidget(self.pnFilter)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.condFilter = QLineEdit(self.centralwidget)
        self.condFilter.setObjectName(u"condFilter")
        self.condFilter.setMinimumSize(QSize(150, 30))
        self.condFilter.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_4.addWidget(self.condFilter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.horizontalSpacer)

        self.btnStartSearch = QPushButton(self.centralwidget)
        self.btnStartSearch.setObjectName(u"btnStartSearch")
        self.btnStartSearch.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.btnStartSearch)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.horizontalSpacer_2)

        self.btnRefreshCache = QPushButton(self.centralwidget)
        self.btnRefreshCache.setObjectName(u"btnRefreshCache")
        self.btnRefreshCache.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.btnRefreshCache)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.btnSaveCond = QPushButton(self.centralwidget)
        self.btnSaveCond.setObjectName(u"btnSaveCond")
        self.btnSaveCond.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.btnSaveCond)


        self.verticalLayout_2.addLayout(self.verticalLayout_5)

        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e09\u83f1\u956d\u5c04\u673a\u52a0\u5de5\u8bb0\u5f55\u67e5\u8be2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u5de5\u578b\u53f7\u7b5b\u9009\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u956d\u5c04\u53c2\u6570\u7b5b\u9009\uff1a", None))
        self.btnStartSearch.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u52a0\u5de5\u8bb0\u5f55", None))
        self.btnRefreshCache.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u672c\u5730\u6570\u636e\u7f13\u5b58", None))
        self.btnSaveCond.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5f53\u524d\u956d\u5c04\u53c2\u6570", None))
    # retranslateUi

