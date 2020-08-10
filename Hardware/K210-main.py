# 作者：蓝一潇
import sensor,image,lcd,time
import KPU as kpu
from Maix import GPIO
from fpioa_manager import fm
import utime
#import os
import network
from machine import UART
import os
import socket
import network
import gc
import video,time
from board import board_info
from fpioa_manager import fm
import lcd
from fpioa_manager import *
from Maix import I2S, GPIO
import audio
import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
from machine import Timer
from machine import I2C
import image
"""
# 音频使能IO
AUDIO_PA_EN_PIN = 32

#注册音频使能IO
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    audio_en=GPIO(GPIO.GPIO1, GPIO.OUT,value=1)

#注册音频控制IO
fm.register(34,  fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35,  fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,  fm.fpioa.I2S0_WS, force=True)

wav_dev = I2S(I2S.DEVICE_0)

"""

# touchscreen
config_touchscreen_support = True
board_m1n = False

i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
if not board_m1n:
    lcd.init()
else:
    lcd.init()
if config_touchscreen_support:
    import touchscreen as ts
    ts.init(i2c)


lv.init()

disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
if board_m1n:
    disp_drv.hor_res = 240
    disp_drv.ver_res = 240
else:
    disp_drv.hor_res = 320
    disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

if config_touchscreen_support:
    indev_drv = lv.indev_drv_t()
    lv.indev_drv_init(indev_drv)
    indev_drv.type = lv.INDEV_TYPE.POINTER
    indev_drv.read_cb = lv_h.read
    lv.indev_drv_register(indev_drv)

# lv.log_register_print_cb(lv_h.log)
lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))
flag = False
lcd.clear()

def fun(obj, event):
    global flag
    flag = True
    print('haha')

_IPADDR = ''
_MAX = -1
#l = lcd.draw_string(110, 120, IPADDR,lcd.BLACK, lcd.WHITE)
def set_IP_PORT(num=None):
    global _IPADDR, _MAX
    if num == '.' or num == ':' or num < 10:
        _IPADDR += '{}'.format(num)
        print('num {}'.format(num))
        if len(_IPADDR) > _MAX:
            _MAX = len(_IPADDR)
    elif num == 10:
        if len(_IPADDR) > 0:
            _IPADDR = _IPADDR[0:-2]
    if len(_IPADDR) < _MAX:
        lcd.draw_string(30, 50, 'http://'+_IPADDR+' '*(_MAX-len(_IPADDR)),lcd.BLACK, lcd.WHITE)
    else:
        lcd.draw_string(30, 50, 'http://'+_IPADDR,lcd.BLACK, lcd.WHITE)
    print(_IPADDR)


jz = 0
count = 4
input_dict = {}
def call_num(num):
    global input_dict, count, jz
    if jz != 0:
        count = jz
        print('count after calibra {}'.format(jz))
        jz = 0
    if num in input_dict and input_dict[num] < count:
        input_dict[num] += 1
    if num in input_dict and input_dict[num] == count:
        set_IP_PORT(num=num)
        input_dict = {}
    if num not in input_dict:
        input_dict = {}
        input_dict[num] = 1



def fun_1(obj, event):
        #print('event is {}'.format(event))
        if event == 0:
            call_num(1)
            #print('number is :1')
            pass
        pass

def fun_2(obj, event):
    #print('event is {}'.format(event))
    if event == 0:
        call_num(2)
        #print('number is :2')
        pass
    pass

def fun_3(obj, event):
    #print('event is {}'.format(event))
    if event == 0:
        call_num(3)
        #print('number is :3')
        pass
    pass

def fun_4(obj, event):
    #print('event is {}'.format(event))
    if event == 0:
        call_num(4)
        #print('number is :4')
        pass
    pass

def fun_5(obj, event):
    if event == 0:
        call_num(5)
    pass

def fun_6(obj, event):
    pass
    if event == 0:
        call_num(6)

def fun_7(obj, event):
    pass
    if event == 0:
        call_num(7)

def fun_8(obj, event):
    pass
    if event == 0:
        call_num(8)

def fun_9(obj, event):
    pass
    if event == 0:
        call_num(9)

def fun_0(obj, event):
    pass
    if event == 0:
        call_num(0)

def fun_del(obj, event):
    if event == 0:
        call_num(10)
    pass

def fun_mh(obj, event):
    pass
    if event == 0:
        call_num(':')

def fun_d(obj, event):
    if event == 0:
        call_num('.')
    pass


def fun_jz(obj, event):
    global jz
    if event == 0:
        jz += 1
        print('jz')

b_w = 50
b_h = 25

scr = lv.obj()
btn = lv.btn(scr)
btn.align(lv.scr_act(), lv.ALIGN.IN_TOP_RIGHT, 0, 0)
btn.set_size(100, 50)
btn.set_event_cb(fun)
label = lv.label(btn)
label.set_text("Start")
label.set_size(20,20)

btn_1 = lv.btn(scr)
btn_1.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 10, 0)
btn_1.set_size(b_w, b_h)
btn_1.set_event_cb(fun_1)
label_1 = lv.label(btn_1)
label_1.set_text("1")
label_1.set_size(20,20)

btn_2 = lv.btn(scr)
btn_2.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 70, 0)
btn_2.set_size(b_w, b_h)
btn_2.set_event_cb(fun_2)
label_2 = lv.label(btn_2)
label_2.set_text("2")
label_2.set_size(20,20)

btn_3 = lv.btn(scr)
btn_3.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 130, 0)
btn_3.set_size(b_w, b_h)
btn_3.set_event_cb(fun_3)
label_3 = lv.label(btn_3)
label_3.set_text("3")
label_3.set_size(20,20)

btn_4 = lv.btn(scr)
btn_4.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 10, -35)
btn_4.set_size(b_w, b_h)
btn_4.set_event_cb(fun_4)
label_4 = lv.label(btn_4)
label_4.set_text("4")
label_4.set_size(20,20)

btn_5 = lv.btn(scr)
btn_5.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 70, -35)
btn_5.set_size(b_w, b_h)
btn_5.set_event_cb(fun_5)
label_5 = lv.label(btn_5)
label_5.set_text("5")
label_5.set_size(20,20)

btn_6 = lv.btn(scr)
btn_6.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 130, -35)
btn_6.set_size(b_w, b_h)
btn_6.set_event_cb(fun_6)
label_6 = lv.label(btn_6)
label_6.set_text("6")
label_6.set_size(20,20)

btn_7 = lv.btn(scr)
btn_7.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 10, -70)
btn_7.set_size(b_w, b_h)
btn_7.set_event_cb(fun_7)
label_7 = lv.label(btn_7)
label_7.set_text("7")
label_7.set_size(20,20)

btn_8 = lv.btn(scr)
btn_8.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 70, -70)
btn_8.set_size(b_w, b_h)
btn_8.set_event_cb(fun_8)
label_8 = lv.label(btn_8)
label_8.set_text("8")
label_8.set_size(20,20)

btn_9 = lv.btn(scr)
btn_9.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 130, -70)
btn_9.set_size(b_w, b_h)
btn_9.set_event_cb(fun_9)
label_9 = lv.label(btn_9)
label_9.set_text("9")
label_9.set_size(20,20)

btn_0 = lv.btn(scr)
btn_0.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 130, 35)
btn_0.set_size(b_w, b_h)
btn_0.set_event_cb(fun_0)
label_0 = lv.label(btn_0)
label_0.set_text("0")
label_0.set_size(20,20)

btn_mh = lv.btn(scr)
btn_mh.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 190, 0)
btn_mh.set_size(b_w, b_h)
btn_mh.set_event_cb(fun_mh)
label_mh = lv.label(btn_mh)
label_mh.set_text(":")
label_mh.set_size(20,20)

btn_del = lv.btn(scr)
btn_del.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 10, 35)
btn_del.set_size(b_w, b_h)
btn_del.set_event_cb(fun_del)
label_del = lv.label(btn_del)
label_del.set_text("DEL")
label_del.set_size(20,20)

btn_j = lv.btn(scr)
btn_j.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 190, 35)
btn_j.set_size(b_w, b_h)
btn_j.set_event_cb(fun_jz)
label_j = lv.label(btn_j)
label_j.set_text("calib")
label_j.set_size(20,20)

btn_d = lv.btn(scr)
btn_d.align(lv.scr_act(), lv.ALIGN.IN_BOTTOM_LEFT, 70, 35)
btn_d.set_size(b_w, b_h)
btn_d.set_event_cb(fun_d)
label_d = lv.label(btn_d)
label_d.set_text(".")
label_d.set_size(20,20)


lv.scr_load(scr)

while True:
    tim = time.ticks_ms()
    lv.tick_inc(5)
    lv.task_handler()
    #print('here {}'.format(time.time()))
    while time.ticks_ms()-tim < 10:
        pass
    #print(flag)
    #time.sleep(1)
    if flag:
        break
print('[OK] IPADDR: {}'.format(_IPADDR))
lcd.clear()

#########################################
SSID='TP-LINK_074E' # WiFi 账号
PWD='lh19910721'  # WiFi 密码

IPADDR = '192.168.3.105'
#IPADDR ='14.215.177.38'
PORT = 7000
#PORT = 80

if _IPADDR != '':
    IPADDR = _IPADDR.split(':')[0]
    print('[INFO]: New IP: {}'.format(IPADDR))
    PORT = int(_IPADDR.split(':')[1])
    print('[INFO]: New Port: {}'.format(PORT))

def speak(name):
    global wav_dev
    player = audio.Audio(path = "/sd/service-yuyin/{}.wav".format(name))
    wav_info = player.play_process(wav_dev)
    wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT ,cycles = I2S.SCLK_CYCLES_32, align_mode = I2S.RIGHT_JUSTIFYING_MODE)
    wav_dev.set_sample_rate(wav_info[1])
    wav_dev.set_sample_rate(44100)
    player.volume(100)
    while True:
        ret = player.play()
        if ret == None:
            print("format error")
            break
        elif ret==0:
            print("end")
            break
    player.finish()

# 音频使能IO
AUDIO_PA_EN_PIN = 32
fm.register(16, fm.fpioa.GPIO1)
KEY = GPIO(GPIO.GPIO1, GPIO.IN)
fm.register(12, fm.fpioa.GPIO0)
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT)
LED_B.value(0)
#fm.register(14, fm.fpioa.GPIO2)
#fm.register(13, fm.fpioa.GPIO1)
LED_R = GPIO(GPIO.GPIO2, GPIO.OUT,value=1)
LED_G = GPIO(GPIO.GPIO1, GPIO.OUT,value=1)
img = None
LED_R.value(1)
LED_G.value(1)



#注册音频使能IO
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    audio_en=GPIO(GPIO.GPIO1, GPIO.OUT,value=1)

#注册音频控制IO
fm.register(34,  fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35,  fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,  fm.fpioa.I2S0_WS, force=True)

wav_dev = I2S(I2S.DEVICE_0)


lcd.init()
#lcd.clear()
#lcd.rotation(1) #由于图像默认是240*320，因此顺时钟旋转90°。
lcd.display(image.Image("neu.jpg"))

#speak('0')
player = audio.Audio(path = "/sd/service-yuyin/{}.wav".format(0))
wav_info = player.play_process(wav_dev)
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT ,cycles = I2S.SCLK_CYCLES_32, align_mode = I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(wav_info[1])
wav_dev.set_sample_rate(44100)
player.volume(100)
while True:
    ret = player.play()
    if ret == None:
        print("format error")
        break
    elif ret==0:
        print("end")
        break
player.finish()

###############################################






###############################################
speak('kaifa')
speak('chushihua')


#while True:
    #print(KEY.value())
    #if KEY.value()==0: #按键被按下接地
       #print('here2')
       #speak('kaifa')

###### WiFi模块初始化 ######
#使能引脚初始化
fm.register(8, fm.fpioa.GPIOHS0, force=True)
wifi_en=GPIO(GPIO.GPIOHS0, GPIO.OUT)

#串口初始化
fm.register(7, fm.fpioa.UART2_TX, force=True)
fm.register(6, fm.fpioa.UART2_RX, force=True)
uart = UART(UART.UART2,115200, read_buf_len=4096)

#使能函数
def wifi_enable(en):
    global wifi_en
    wifi_en.value(en)

#使能wifi模块
wifi_enable(1)
time.sleep(1)

#构建WiFi对象
wlan = network.ESP8285(uart)

#正在连接印提示
print("[STATUS]: Connecting WiFi...")

#print(wlan.scan())

#连接网络
max_try_time = 5
try_time = 0
flag = False
while try_time <= max_try_time and not flag:
    try_time += 1
    try:
        wlan.connect(SSID,PWD)
        flag = True
        speak('wifiok')
    except Exception as e:
        print('[ERROR]: {}'.format(e))
        speak('wifierror')
        #sys.exit(0)
        time.sleep(1)
if not flag:
    speak('wifimultierror')

if flag:
    print('[STATUS]: WiFi Ok!')

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)  #摄像头后置方式

clock = time.clock()

#模型分类，按照20class顺序
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

#下面语句需要将模型（20class.kfpkg）烧写到flash的 0x500000 位置
task = kpu.load(0x500000)

#将模型放在SD卡中。
#task = kpu.load("/sd/20class.kmodel") #模型SD卡上

#网络参数
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

#初始化yolo2网络，识别可信概率为0.7（70%）
a = kpu.init_yolo2(task, 0.6, 0.3, 5, anchor)

def send_pic(filename, ip='192.168.3.105', port=12345):
    global IPADDR, PORT
    addr = (IPADDR, PORT)
    sock = socket.socket()
    sock.connect(addr)
    sock.settimeout(20)
    f = open(filename,"rb")
    count = 1
    sock.send('PICNAME/{}'.format(filename.split('/')[-1]))
    while True:
        count += 1
        print('[COUNT]: {}'.format(count))
        _img = f.read(4096)
        if not _img or (len(_img) == 0):
            sock.send('OVER')
            print('[STATUS]: Over.')
            break
        sock.send(_img)
        #time.sleep(0.1)
    f.close()
    sock.close()
    return

def send_msg(msg):
    global IPADDR, PORT
    addr = (IPADDR, PORT)
    sock = socket.socket()
    sock.connect(addr)
    sock.settimeout(20)
    sock.send('MSG/{}'.format(msg))
    sock.close()
    return




def alarm():
    global LED_R, img
    #for i in range(5):
        #LED_R.value(0)
        #time.sleep(0.3)
        #LED_R.value(1)
        #time.sleep(0.3)
    print(img.size())
    filename = '/sd/alarm_img/alarm-snapshot-{}.bmp'.format(time.time())
    img.save(filename, quality=1)
    LED_R.value(0)
    send_pic(filename)
    LED_R.value(1)


def _alarm():
    global LED_R, LED_G
    #for i in range(5):
        #LED_R.value(0)
        #LED_G.value(0)
        #time.sleep(0.3)
        #LED_R.value(1)
        #LED_G.value(1)
        #time.sleep(0.3)

def alarm_close_over():
    pass


def sample():
    img.save('/sd/sample_img/sample-snapshot-{}.bmp'.format(time.time()))


# test
max_try_time = 10
try_time = 0
flag = False
while try_time <= 10 and not flag:
    try_time += 1
    try:
        #send_pic('1.jpg')
        send_msg('conn')
        flag = True
        speak('serverok')
    except Exception as e:
        print('[ERROR]: {}'.format(e))
        speak('servererror')
        time.sleep(1)
if not flag:
    #sys.exit(0)
    speak('multierror')

#def fun(KEY):
    #print('here')
    #utime.sleep_ms(10) #消除抖动
    #if KEY.value()==0: #确认按键被按下
        #speak('kaifa')



#KEY.irq(fun, GPIO.IRQ_FALLING)
lcd.rotation(0)
LED_B.value(1)
while(True):
    try:
        clock.tick()
        img = sensor.snapshot()
        code = kpu.run_yolo2(task, img) #运行yolo2网络
        histogram = img.get_histogram()
        #percentile = histogram.get_percentile()
        #print(percentile.value())
        stat_dict = histogram.get_statistics()
        if stat_dict[0] < 10 and stat_dict[1] < 10 and stat_dict[2] < 10 and stat_dict[3] < 10:
            _alarm()
            try:
                send_msg('cover')
            except:
                print('[FATAL]: Loss one msg.')
            speak('2')

        if int(time.time()) % 20 == 0:
            sample()
            try:
                send_msg('heartbeat')
            except Exception as e:
                print('[ERROR]: {}'.format(e))


        pass
        if KEY.value()==0: #按键被按下接地
            speak('kaifa')
        else:
            pass



        if code:
            for i in code:
                a=img.draw_rectangle(i.rect())
                a = lcd.display(img)
                if classes[i.classid()] == 'person':
                    try:
                        send_msg('find')
                    except:
                        print('[FATAL]: loss one msg.')
                    speak('1')
                    try:
                        alarm()
                    except:
                        print('[FATAL]: Loss one pic.')
                lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                lcd.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
        else:
            a = lcd.display(img)

        print(clock.fps())#打印FPS
    except Exception as e:
        print('[FATAL]: {}'.format(e))
        speak('restart')
