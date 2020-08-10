# -*- coding: utf-8 -*-
# 作者：蓝一潇
import sys  # 导入系统
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QTextBrowser
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import random
import hashlib
import threading
import requests
from flask import *
import socket
import socket
from db_manager import *

class Worker(QThread):
    sinOut = pyqtSignal(str) # 自定义信号，执行run()函数时，从相关线程发射此信号

    def __init__(self,ip, parent=None, PREFIX='monitor_alarm'):
        super(Worker, self).__init__(parent)
        self.ip = ip
        self.s = socket.socket()
        self.PREFIX = PREFIX
        self.last_heartbeat = -1

    def __del__(self):
        self.working = False
        self.wait()

    def get_port(self):
        # s = 0
        # while s < 8:
        #     self.sinOut.emit('{}'.format(s))
        #     s += 1
        #     time.sleep(2)


        PORT = 7000
        while True:
            try:
                self.s.bind((self.ip, PORT))
                print('[INFO]: Now port is {}'.format(PORT))
                self.sinOut.emit('PORT/{}'.format(PORT))
                self.sinOut.emit('_0')
                break
            except Exception as e:
                print('[ERROR]: Port is in use. {}'.format(e))
                PORT += 1

    def run(self):
        self.get_port()
        self.s.listen(5)
        self.sinOut.emit('_1')
        try:
            while True:
                conn, address = self.s.accept()  # 一定要放在大循环外面！阻塞等待
                name = ''
                ret = ''
                while True:
                    try:
                        print('new request from:{}'.format(address))
                        conn.settimeout(20)
                        res = conn.recv(2048)
                        print(res)
                        if 'OVER' in res:
                            with open(name, 'wb') as f:
                                f.write(ret)
                                f.close()
                                insert(5)
                                self.sinOut.emit('5/{}'.format(name))
                            print('[STATUS]: Get pic.')
                            break

                        if 'PICNAME' in res:
                            name = self.PREFIX + '/' + res.split('/')[1]
                            print('[STATUS]: Pic name is: {}.'.format(name))
                            with open('STATUS', 'wb') as f:
                                f.write('1')
                                f.close()
                                self.sinOut.emit('3')
                                insert(3, path=name)
                            continue
                        if 'MSG' in res:
                            msg = res.split('/')[1]
                            print(msg)
                            if msg == 'conn':
                                self.sinOut.emit('6')
                                insert(6)
                            if msg == 'find':
                                self.sinOut.emit('1')
                                insert(1)
                            if msg == 'cover':
                                self.sinOut.emit('2')
                                insert(2)
                            if msg == 'heartbeat':
                                self.last_heartbeat = time.time()
                                self.sinOut.emit('7')
                                insert(10)
                            break
                        ret += bytes(res)
                        print('[STATUS]: Receive a part.')
                    except Exception as e:
                        print('[ERROR]: {}. Give up for new request.'.format(e))
                        if ret != '':
                            with open(name, 'wb') as f:
                                f.write(ret)
                                f.close()
                            self.sinOut.emit('4/{}'.format(name))
                            print('[STATUS]: Get a uncomplete pic.')
                            insert(4)
                        break
        finally:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            del self.s

class FirstUi(QMainWindow):  # 第一个窗口类
    def __init__(self, ip, count=60, timeout=30):
        super(FirstUi, self).__init__()
        self._echo = ''
        self._count = 2253
        self.r = None
        self.b = 1000
        self.language = 0
        self.ip = ip
        self.thread = Worker(ip)
        # r = hashlib.sha256(str(random.random())).hexdigest()
        # print('self addr: {}'.format(r))
        # self.r = r
        self.thread.sinOut.connect(self.interrupt1)
        self.thread.start()
        self.last_heart = -1
        # self.countdown1 = 10 # 30
        # self.countdown2 = 5 # 15
        self.count = count
        self.timeout = timeout
        self._count = 0
        self.in_recv = False
        self.init_ui()

    def init_ui(self):

        self.resize(800, 400)  # 设置窗口大小
        self.setWindowTitle('东北大学智能监控系统')  # 设置窗口标题

        self.lable1 = QLabel('<h1>东北大学智能监控</h1>', self)
        self.lable1.setGeometry(330, 20, 300, 50)

        self.lable3 = QLabel('<h2>东北大学计算机学院</h2>', self)
        self.lable3.setGeometry(350, 60, 300, 25)

        self.lable4 = QLabel('地址 : {} | 端口 : {}\n请在监控设备上输入\n相同ip与端口进行配对'.format(self.ip, '正在初始化...'), self)
        self.lable4.setGeometry(550, 15, 300, 100)

        self.lable5 = QLabel('事件:', self)
        self.lable5.setGeometry(240, 70, 300, 25)

        self.lable6 = QLabel('<h2>监控画面</h2>', self)
        self.lable6.setGeometry(30, 50, 300, 25)

        self.lable7 = QLabel('', self)
        self.lable7.setGeometry(30, 100, 200, 150)

        self.lable10 = QLabel('<h2>状态:</h2>', self)
        self.lable10.setGeometry(30, 320, 300, 25)

        self.lable11 = QLabel('<h1>正在初始化...</h1>', self)
        self.lable11.setGeometry(30, 340, 500, 50)

        self._prefix = """        事件|   状态码  |   时间  |  源（如果有）
-----------------------------------------------------------------------    
        """
        self._echo = ''

        self.tb = QTextBrowser(self)
        self.tb.setText(self._echo)
        self.tb.setGeometry(240, 100, 500, 220)

        self.btn5 = QPushButton('刷新', self)  # 设置按钮和按钮名称
        self.btn5.setGeometry(320, 320, 100, 25)  # 前面是按钮左上角坐标，后面是窗口大小
        self.btn5.clicked.connect(self.slot_btn_function)  # 将信号连接到槽

        self.lable2 = QLabel('当前时间: 正在获取...', self)
        self.lable2.setGeometry(450, 320, 300, 25)

        self._lable = QLabel('作者： 东北大学 蓝一潇 魏景行 黎芷余', self)
        self._lable.setGeometry(530, 370, 300, 25)

        self.timer = QBasicTimer()  # QTimer()貌似不行，不知何故？
        self.timer.start(1000, self)

    def set_status(self, msg):
        self.lable11.setText('<h1>{}</h1>'.format(msg))

    def slot_btn_function(self):
        self._echo = ''
        self.tb.setText(self._prefix)
        pass

    def timerEvent(self, event):
        pass
        if event.timerId() == self.timer.timerId():
            self.lable2.setText('当前时间: {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

            if self.in_recv:
                return


            if self._count < self.count:
                self._count += 1
            else:
                self._count = 0
                if time.time() - self.last_heart > self.timeout and self.last_heart != -1:
                    self.append_echo('监控设备失联！         ', status=7)
                    self.set_status('❌监控断开！正在接受新的连接...')
                    insert(9)

    def add_image(self, name):
        jpg = QPixmap('monitor_alarm/{}'.format(name)).scaled(self.lable7.width(), self.lable7.height())
        self.lable7.setPixmap(jpg)




    def append_echo(self, msg, status=None, path=None):

        self._echo = """{}|  {}  | {} |  {}
-----------------------------------------------------------------------
        """.format(msg, '' if status is None else status, time.strftime("%Y-%m-%d %H:%M:%S"), '' if path is None else path) + self._echo
        self.tb.setText(self._prefix+self._echo)

    def interrupt1(self, sig):
        if sig == '_0':
            self.append_echo('系统正在初始化...     ')
            insert(8)
        if sig == '_1':
            self.append_echo('初始化完成。          ')
            self.set_status('正在接受监控连接信息... ')
            insert(9)
        if sig == '0':
            self.append_echo('监控画面正常。        ', status=0)
            self.set_status('正在监控...')
        if sig == '1':
            self.append_echo('画面中出现人影！      ', status=1)
            self.set_status('⚠️警告！发现危险！')
        if sig == '2':
            self.append_echo('摄像头被遮挡！        ', status=2)
            self.set_status('⚠️警告！摄像头被遮挡！')
        if sig == '3':
            self.append_echo('正在接受监控数据！     ', status=3)
            self.in_recv = True
        if '4' in sig:
            self.append_echo('传输中途断开！        ', status=4, path=sig.split('/')[-1])
            self.add_image(name=sig.split('/')[-1])
            self.set_status('正在监控...')
            self.in_recv = False
        if '5' in sig:
            self.append_echo('图像传输完毕！         ', status=5, path=sig.split('/')[-1])
            self.add_image(name=sig.split('/')[-1])
            self.in_recv = False
        if sig == '6':
            self.append_echo('监控设备已连接。       ', status=6)
            self.set_status('正在监控...')
        if sig == '7':
            self.last_heart = self.thread.last_heartbeat
            self.append_echo('监控keep-alive       ', status=10)
            self.set_status('正在监控...')

        if 'PORT' in sig:
            self.lable4.setText('地址 : {} | 端口 : {}\n请在监控设备上输入\n相同ip与端口进行配对'.format(self.ip, sig.split('/')[1]))


def get_a_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    print('[INFO]: Host ip is: {}'.format(ip))

    del s

    return ip


if __name__ == '__main__':

    appmain = QApplication(sys.argv)
    w = FirstUi(get_a_ip())  # 将第一和窗口换个名字
    w.show()  # 将第一和窗口换个名字显示出来
    sys.exit(appmain.exec_())  # app.exet_()是指程序一直循环运行直到主窗口被关闭终止进程（如果没有这句话，程序运行时会一闪而过）
