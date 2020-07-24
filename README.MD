# 基于K210的智能监控系统

## 作者：蓝一潇

## 说明
项目源码分为两个模块，硬件模块代码以及服务端模块代码。两个模块都使用python进行编写（其中硬件使用了micropython）
硬件模块代码K210-main.py运行在K210开发板上，可以使用sipeed ide连接开发板并运行程序，也可以通过串口终端将源码保存至开发板的boot.py文件中，当开发板上电后，会自动运行源代码。需要提前将shibie.kmodel、20class.kmodel、sample_img文件夹、service-yuyin文件夹、neu.jpg拷贝到K210的SD卡上。
服务端代码可以直接在PC命令行中运行。输入 ```python client-server.py```即可运行。运行程序后，服务端会弹出GUI界面，也会显示本机ip地址以及服务端口，需要在硬件端输入服务端显示的套接字，方可将硬件端与服务端进行连接。
服务端需要提前在PC上安装python的依赖库有：
1. socket
2. sqlite3
3. PyQt5
