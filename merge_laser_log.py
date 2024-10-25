#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from datetime import date,timedelta
from os import path
import re

# log_path=[
#     {"machineID":"D07#","logPath":r"U:\激光钻机\一厂激光钻机\7#"},
#     {"machineID":"D08#","logPath":r"U:\激光钻机\一厂激光钻机\8#"},
#     {"machineID":"D09#","logPath":r"U:\激光钻机\一厂激光钻机\9#"},
#     {"machineID":"D10#","logPath":r"U:\激光钻机\一厂激光钻机\10#"},
#     {"machineID":"D11#","logPath":r"U:\激光钻机\一厂激光钻机\11#"},
#     {"machineID":"D12#","logPath":r"U:\激光钻机\一厂激光钻机\12#"},
#     {"machineID":"Q01#","logPath":r"U:\激光钻机\二厂激光钻机\Q01"},
#     {"machineID":"Q02#","logPath":r"U:\激光钻机\二厂激光钻机\Q02"}
# ]

log_path=[
    {"machineID":"D07#","logPath":r"\\172.29.250.14\DevData1\激光钻机\一厂激光钻机\7#"},
    {"machineID":"D08#","logPath":r"\\172.29.250.14\DevData1\激光钻机\一厂激光钻机\8#"},
    {"machineID":"D09#","logPath":r"\\172.29.250.14\DevData1\激光钻机\一厂激光钻机\9#"},
    {"machineID":"D10#","logPath":r"\\172.29.250.14\DevData1\激光钻机\一厂激光钻机\10#"},
    {"machineID":"D11#","logPath":r"\\172.29.250.14\DevData1\激光钻机\一厂激光钻机\11#"},
    {"machineID":"D12#","logPath":r"\\172.29.250.14\DevData1\激光钻机\一厂激光钻机\12#"},
    {"machineID":"Q01#","logPath":r"\\172.29.250.14\DevData1\激光钻机\二厂激光钻机\Q01"},
    {"machineID":"Q02#","logPath":r"\\172.29.250.14\DevData1\激光钻机\二厂激光钻机\Q02"}
]

start_date=date(2024,9,15)
end_date=date(2024,10,15)
filter=r'98181A0\-\d+'

save_work_file=r'D:\镭射加工记录.csv'
save_cond_file=r'D:\镭射参数记录.csv'


def fetch_log(machinID,file_path,save_file,filter=''):
    print(file_path)
    r=re.compile(filter,re.I)
    if path.isfile(file_path):
        with open(file_path, 'r', encoding='gbk') as log_file:
            log_file.readline()
            for line in log_file:
                if r.search(line):
                    save_file.write(f"{machinID},{line}")

current_date=start_date
with open(save_work_file, 'w', encoding='gbk', newline='') as work_file:
    work_file.write("机台,Stage,日期,时间,管理No.,序列号,伸缩率 X,伸缩率 Y,主程序的程序编号,条件文件,状态,错误内容,偏置X,偏置Y,θ,状态,再开始状态,停止程序块,结束程序块,区块编号,手动模式,工件补偿类型,P1X,P1Y,P2X,P2Y,P3X,P3Y,P4X,P4Y,P5X,P5Y,伸缩率/设定率 X,伸缩率/设定率 Y,PRG START TIME,RateP1-P2,RateP3-P4,RateP2-P3,RateP1-P4,RateP1-P3,RateP2-P4\r\n")
    with open(save_cond_file, 'w', encoding='gbk', newline='') as cond_file:
        cond_file.write("机台,日期,时间,加工程序,条件文件,条件编号,输出功率,频率,脉宽,脉级,速度,脉冲数,光罩编号,B/C,G,准直NO.,基准倍率,当前倍率,基准能量,测量频率,容许范围,,光路类型NO.,笔记\r\n")
        while current_date<=end_date:
            year=f"{current_date.year}"[-2:]
            for machineInfo in log_path:
                fetch_log(machineInfo["machineID"],path.join(machineInfo["logPath"],f"{current_date.year}{current_date.month:02d}",f"sinsyuku_{year}{current_date.month:02d}{current_date.day:02d}.log"),work_file,filter)
                fetch_log(machineInfo["machineID"],path.join(machineInfo["logPath"],f"{current_date.year}{current_date.month:02d}",f"cndselct_{year}{current_date.month:02d}{current_date.day:02d}.log"),cond_file,filter)
            current_date+=timedelta(days=1)
