#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import sqlite3
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QIcon
import icon_rc

# Loading config
CONFIG_FILE=r'config.json'
with open(CONFIG_FILE,'r',encoding='utf-8') as f:
    CONFIG=json.load(f)

# Sqlite3 datetime adapter
def date_to_str(date):
    return date.strftime('%Y/%m/%d %H:%M:%S')

def str_to_date(str):
    return datetime.strptime(str.replace('-','/'), '%Y/%m/%d %H:%M:%S')

class LaserCondition(object):
    def __init__(self) -> None:
        self.name=''
        self.lines = []
        self.lines.append(['@Attribute=<TOPHAT>\r\n'])
        self.updated_rows = []
        for _ in range(50):
            self.lines.append(
                '5600,100,7.0,71000,1,1,1,C,0,0.000,100,500,S,,,0,\r\n'.split(','))

    def set_cond(self, rowId: int, cond: list) -> bool:
        rowId = int(rowId)
        if 0 < rowId <= 50:
            row = self.lines[rowId]
            row[0] = cond[0]            # 输出功率
            row[1] = cond[1]            # 频率
            row[2] = cond[2]            # 脉宽
            row[3] = cond[4]            # 速度
            row[4] = cond[5]            # 脉冲数
            row[5] = cond[6]            # 光罩编号
            row[6] = cond[9]            # 准直NO.
            row[7] = cond[7]            # B/C 模式
            row[8] = cond[8]            # Group编号
            row[9] = cond[12]           # 基准能量
            row[10] = cond[13]          # 测量频率
            row[11] = str(int(
                float(cond[14])*100     # 容许范围,加工记录中为百分比带两位小数
            ))
            row[12] = cond[3]           # 脉冲等级
            row[13] = cond[17].strip()  # 笔记备注
            row[14] = cond[15]
            row[15] = cond[16]          # 光路类型NO.
            row[16] = '\r\n'
            if rowId not in self.updated_rows:
                self.updated_rows.append(rowId)
            return True
        return False

    def is_updated(self, rowId: int) -> bool:
        # 检查指定的行参数是否有更新过
        rowId = int(rowId)
        return (rowId in self.updated_rows)

    def create_model(self):
        model=[]
        for v in self.lines[1:]:
            model.append(['' if v[8]=='0' else v[8],v[2],v[9],v[4],v[5],v[6],v[13]])
        return model

    def save_as(self, filePath) -> None:
        # 将参数保存为指定的文件
        with open(filePath, 'w', newline='') as f:
            for line in self.lines:
                f.write(','.join(line))

    def update_from_log(self, filePath, drillDateTime, prgName, condName):
        # 从指定的参数加工记录中载入加工参数

        if type(drillDateTime) is str:
            drillDateTime=str_to_date(drillDateTime)

        # 清空当前参数
        self.updated_rows = []
        for i in range(1,51):
            self.lines[i]='5600,100,7.0,71000,1,1,1,C,0,0.000,100,500,S,,,0,\r\n'.split(',')

        # 读取加工参数记录
        with open(filePath, 'r', encoding='gb2312') as f:
            lines=f.readlines()
        lines=lines[1:]      #删除表头
        lines=lines[::-1]    #数据反向

        flag = False
        for line in lines:
            row = line.split(',')
            if len(row) >= 23:
                curTime = str_to_date('{} {}'.format(
                    row[0].replace('-', '/'), row[1]))
                curPrg = row[2].split('\\')[-1].upper()
                curCond = row[3].split('\\')[-1].upper()
                if curCond[-4:]=='.CND':
                    curCond=curCond[:-4]
                curRow = int(row[4])
                if curTime <= drillDateTime and curPrg == prgName.upper() and curCond == condName.upper() and curRow > 0:
                    if self.is_updated(curRow):
                        break
                    self.set_cond(curRow, row[5:])
                    flag = True
                else:
                    if flag:
                        break
        return flag

class Database(object):
    def __init__(self,database,machines):
        self.database=database
        self.session=None
        self.machines=machines
        self.datetime={}

    def open(self):
        self.close()
        if os.path.isfile(self.database):
            create_table=False
        else:
            create_table=True
        self.session = sqlite3.connect(self.database)
        cursor = self.session.cursor()
        if create_table:
            cursor.execute('''CREATE TABLE sinstatis
                (machine Text,datetime Text, lot Text,prg Text COLLATE NOCASE,cond Text COLLATE NOCASE);''')
            self.session.commit()

    def close(self):
        try:
            self.session.close()
            self.session=None
        except Exception:
            pass

    def get_cndlog_path(self,machineId,datetime):
        logPath=None
        for machine in self.machines:
            if machineId==machine['name']:
                logPath=machine['logPath']
        if not logPath:
            return ''
        
        yyyy=datetime[:4]
        yy=yyyy[-2:]
        mm=datetime[5:7]
        dd=datetime[8:10]
        yyyymm=yyyy+mm
        yymmdd=yy+mm+dd
        return os.path.join(logPath,f'{yyyymm}',f'cndselct_{yymmdd}.log')

    def get_cnd(self,machineId,datetime, prgName, condName):
        logPath=self.get_cndlog_path(machineId,datetime)
        if not logPath:
            return None
        cond=LaserCondition()
        if cond.update_from_log(logPath,datetime,prgName,condName):
            return cond
        else:
            return None


    def update_laser_log(self,callback=None):
        self.update_datetime()
        for machine in self.machines:
            latest_time=self.datetime[machine['name']]
            yyyy=latest_time[:4]
            yy=yyyy[-2:]
            mm=latest_time[5:7]
            dd=latest_time[8:10]
            yyyymm=yyyy+mm
            yymmdd=yy+mm+dd
            for folder in os.scandir(machine['logPath']):
                if folder.is_dir() and len(folder.name)==6 and folder.name.isnumeric() and folder.name>=yyyymm:
                    for file in os.scandir(folder.path):
                        if file.name.startswith('Sinstatis_'):
                            if callback:
                                callback.showMessage('正在扫描文件：'+file.path,3000)
                                App.processEvents()
                            file_date=file.name[10:16]
                            if file_date>=yymmdd:
                                self.load_log_file(machine['name'],file.path,latest_time)
            self.session.commit()

    def load_log_file(self,machine_name,file_path,latest_time):
        with open(file_path, 'r', encoding='gbk') as log_file:
            cursor=self.session.cursor()
            log_file.readline()
            for line in log_file:
                data=line.split(',')
                if len(data)>13:
                    date=data[1]
                    time=data[2]
                    datetime=date_to_str(str_to_date(f'{date} {time}'))
                    if datetime>latest_time:
                        lot=data[3]
                        prg=data[12].split('\\')[-1]
                        cond=data[13]
                        if cond[-4:].lower()=='.cnd':
                            cond=cond[:-4]
                        cursor.execute(
                            '''INSERT INTO sinstatis (machine,datetime,lot,prg,cond) VALUES (?,?,?,?,?)''',
                            (machine_name,datetime,lot,prg,cond)
                        )
            cursor.close()

    def update_datetime(self):
        # 更新数据库中的每台镭射机的最新加工时间
        self.datetime={}
        for row in self.session.execute('SELECT machine,MAX(datetime) FROM sinstatis GROUP BY machine;'):
            self.datetime[row[0]]=row[1]
        for machine in self.machines:
            if machine['name'] not in self.datetime:
                self.datetime[machine['name']]='0000/00/00 00:00:00'

    def search_log(self,prg='',cond=''):
        if prg:
            if cond:
                SQL='SELECT datetime,machine,prg,cond FROM sinstatis WHERE prg LIKE ? AND cond LIKE ? ORDER BY datetime DESC LIMIT 500;'
                query=(prg,cond)
            else:
                SQL='SELECT datetime,machine,prg,cond FROM sinstatis WHERE prg LIKE ? ORDER BY datetime DESC LIMIT 500;'
                query=(prg,)
        else:
            if cond:
                SQL='SELECT datetime,machine,prg,cond FROM sinstatis WHERE cond LIKE ? ORDER BY datetime DESC LIMIT 500;'
                query=(cond,)
            else:
                raise ValueError('必须提供搜索的型号或参数！')

        return self.session.execute(SQL,query).fetchall()


class TblLaserLogModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], parent=None):
        super().__init__(parent)
        self.mydata = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        columns=[
            '时间',
            '机台',
            '程序',
            '参数'
        ]
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return columns[section]
            else:
                return str(section+1)

    def columnCount(self, parent=None):
        return 4

    def rowCount(self, parent=None):
        return len(self.mydata)

    def data(self, index: QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.mydata[row][col])


class TblLaserCondModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], parent=None):
        super().__init__(parent)
        self.mydata = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        columns=[
            '分组',
            '脉宽',
            '能量',
            '发数',
            '光圈',
            '准直镜',
            '备注'
        ]
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return columns[section]
            else:
                return str(section+1)

    def columnCount(self, parent=None):
        return 7

    def rowCount(self, parent=None):
        return len(self.mydata)

    def data(self, index: QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.mydata[row][col])

class Ui_MainWindow(object):
    def setupUi(self, MainWindow,config):
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

        self.init_signal_connect()
        self.config=config
        self.cond=None
        self.logs=[[]]

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_signal_connect(self):
        self.btnStartSearch.clicked.connect(self.search_log)
        self.btnRefreshCache.clicked.connect(self.refresh_database)
        self.btnSaveCond.clicked.connect(self.save_laser_cond)
        self.pnFilter.returnPressed.connect(self.search_log)
        self.condFilter.returnPressed.connect(self.search_log)
        self.tblLaserLog.clicked.connect(self.search_cond)
        self.tblLaserLog.doubleClicked.connect(self.search_cond)

    def disable_btn(self):
        self.btnStartSearch.setDisabled(True)
        self.btnRefreshCache.setDisabled(True)
        self.btnSaveCond.setDisabled(True)
        self.pnFilter.setDisabled(True)
        self.condFilter.setDisabled(True)

    def enable_btn(self):
        self.btnStartSearch.setDisabled(False)
        self.btnRefreshCache.setDisabled(False)
        self.btnSaveCond.setDisabled(False)
        self.pnFilter.setDisabled(False)
        self.condFilter.setDisabled(False)

    def search_log(self):
        self.disable_btn()
        db=Database(self.config['database'],self.config['machines'])
        db.open()
        self.logs=db.search_log(prg=self.pnFilter.text(),cond=self.condFilter.text())
        model=TblLaserLogModel(self.logs)
        self.tblLaserLog.setModel(model)
        self.tblLaserLog.resizeColumnsToContents()
        self.statusbar.showMessage('一共找到 {} 条生产记录。'.format(model.rowCount()))
        db.close()
        self.enable_btn()

    def refresh_database(self):
        self.disable_btn()
        db=Database(self.config['database'],self.config['machines'])
        db.open()
        db.update_laser_log(callback=self.statusbar)
        db.close()
        QMessageBox.information(None,'更新完成','已经完成本地数据库缓存的更新！',QMessageBox.Yes)
        self.enable_btn()
    
    def search_cond(self,index:QModelIndex):
        db=Database(self.config['database'],self.config['machines'])
        item=self.logs[index.row()]
        self.cond=db.get_cnd(item[1],item[0],item[2],item[3])
        self.cond.name=item[3]+'.cnd'
        if self.cond:
            model=TblLaserCondModel(self.cond.create_model())
            self.statusbar.showMessage('当前镭射参数：'+item[3])
        else:
            model=TblLaserCondModel()
            self.statusbar.showMessage('')
        self.tblLaserCond.setModel(model)
        self.tblLaserCond.resizeColumnsToContents()


    def save_laser_cond(self):
        if self.cond:
            filePath,_=QFileDialog.getSaveFileName(None,'保存镭射参数',self.cond.name,'参数文件 (*.cnd)')
            if filePath:
                self.cond.save_as(filePath)
                QMessageBox.information(None,'完成','当前镭射加工参数保存成功！',QMessageBox.Ok)
        else:
            QMessageBox.information(QMessageBox.Critical,'错误','请先选择镭射加工参数！',QMessageBox.Ok)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "三菱镭射机加工记录查询"))
        self.label.setText(_translate("MainWindow", "加工型号筛选："))
        self.label_2.setText(_translate("MainWindow", "镭射参数筛选："))
        self.btnStartSearch.setText(_translate("MainWindow", "搜索加工记录"))
        self.btnRefreshCache.setText(_translate("MainWindow", "刷新本地数据缓存"))
        self.btnSaveCond.setText(_translate("MainWindow", "保存当前镭射参数"))

if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    icon=QIcon(":/icon.ico")
    App.setWindowIcon(icon)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,CONFIG)
    MainWindow.show()
    sys.exit(App.exec_())