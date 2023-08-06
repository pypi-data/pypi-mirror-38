from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import json
import pygame
import time
import urllib
import random
import math

parwidth = 600

flg = 0
fff = 0
f = 0
border = 0
borderr = 0
angle = 1
direction = 1

ipStr = 'http://jiaoxue.vipcode.cn/'

global filename
filename = ""

# 创建窗口
class PyQt5_QDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("dialog")
        global parwidth
        parwidth = self.width()+200
    def setBackgroundColor(self, color):
        self.setStyleSheet("#dialog{background-color:"+color+"}")
    def setBackground(self, image_name):
        self.setStyleSheet("#dialog{border-image:url(RESOURCE/drawable/"+image_name+")}")

    def setResize(self, width, height):
        self.resize(width, height)
    
    def addBodyButton(self,label):
        self.bodylabel=label
        self.head = PyQt5_QPushButton(self, 400, 300, 160, 130)
        self.head.setBackgroundColor("rgba(100,0, 200, 0)")

        self.body = PyQt5_QPushButton(self, 445, 430, 70, 80)
        self.body.setBackgroundColor("rgba(100,0, 200, 0)")

        self.leftArm = PyQt5_QPushButton(self, 420, 430, 40, 30)
        self.leftArm.setBackgroundColor("rgba(0,0, 0, 0)")

        self.rightArm = PyQt5_QPushButton(self, 505, 430, 50, 30)
        self.rightArm.setBackgroundColor("rgba(0,0, 0, 0)")

        self.leftFoot = PyQt5_QPushButton(self, 440, 500, 30,30)
        self.leftFoot.setBackgroundColor("rgba(0,0, 0, 0)")

        self.rightFoot = PyQt5_QPushButton(self, 500, 500, 30, 30)
        self.rightFoot.setBackgroundColor("rgba(0,0, 0, 0)")

        self.head.clicked.connect(self.headClicked)
        self.leftArm.clicked.connect(self.armClicked)
        self.rightArm.clicked.connect(self.armClicked)
        self.rightFoot.clicked.connect(self.rightFootClicked)
        self.leftFoot.clicked.connect(self.leftFootClicked)
        self.body.clicked.connect(self.bodyClicked)
    def armClicked(self):
        self.neibu2('main_arm')
        # music = PyQt5_QMediaPlayer()
        # music.prepare_audio('main_arm.wav')
        # music.play()
        # 播放
        self.neibu1('main_arm')
    def leftFootClicked(self):
        self.neibu2('main_leftFoot')
        self.neibu1('main_leftFoot')
    def rightFootClicked(self):
        self.neibu2('main_rightFoot')
        self.neibu1('main_rightFoot')
    def bodyClicked(self):
        self.neibu2('main_body')
        self.neibu1('main_body')
    def headClicked(self):
        self.neibu2('main_head')
        self.neibu1('main_head')
     # 播放的gif
    def neibu2(self, gif_name):
        # 确定要播放的gif
        self.neigif = PyQt5_QMovie(gif_name+'.gif')
        # 给gif设置大小
        self.neigif.setScaledSize(self.bodylabel.size())
        # 确定label播放哪个neigif 
        self.bodylabel.setMovie(self.neigif)
        # 播放neigif
        self.neigif.start()
        self.frameCount = self.neigif.frameCount()
        # neigif帧数改变事件
        self.neigif.frameChanged.connect(self.neibu3)
    def neibu3(self):
        # 让帧数自减一
        self.frameCount -= 1
        # 如果帧数为0
        if self.frameCount == 0:
            # 停止播放当前neigif
            self.neigif.stop()
            # 继续播放主界面neigif
            self.neigif = PyQt5_QMovie('main_lion.gif')
            self.neigif.setScaledSize(self.bodylabel.size())
            # 确定label播放哪个neigif 
            self.bodylabel.setMovie(self.neigif)
            # 播放neigif
            self.neigif.start()
       # 播放音效
    def neibu1(self, auido_name):
        # 对音乐处理模块进行初始化
        music = PyQt5_QMediaPlayer()
        # 加载播放的声音文件
        music.prepare_audio(auido_name+'.wav')
        # 播放
        music.play()

# 创建按钮
class PyQt5_QPushButton(QPushButton):
    def __init__(self, QWidget, x = 0, y = 0, width = 113, height = 32):
        super().__init__(QWidget)
        self.setGeometry(x, y, width, height)

    def setBackground(self, image_name):
        self.setStyleSheet(self.styleSheet()+"QPushButton{border-image:url(RESOURCE/drawable/" 
            + image_name +")}")

    def setPressedBackground(self, image_name):
        self.setStyleSheet(self.styleSheet()+"QPushButton:pressed{border-image:url(RESOURCE/drawable/" 
            + image_name +")}")
    
    def setBackgroundColor(self, color):
        self.setStyleSheet(self.styleSheet()+"QPushButton{background-color:"+color+"}")

    def setTextColor(self, color):
        self.setStyleSheet(self.styleSheet()+"QPushButton{color:"+color+"}")

    def setPressedTextColor(self, color):
        self.setStyleSheet(self.styleSheet()+"QPushButton:pressed{color:"+color+"}")
    
    def setFontSize(self, size):
        font = QFont()
        font.setPixelSize(size)
        self.setFont(font)

# 创建输入框
class PyQt5_QLineEdit(QLineEdit):
    Password = QLineEdit.Password
    Normal = QLineEdit.Normal
    NoEcho = QLineEdit.NoEcho
    PasswordEchoOnEdit = QLineEdit.PasswordEchoOnEdit

    def __init__(self, QWidget, x =0, y = 0, width = 113, height = 21):
        super().__init__(QWidget)
        self.setGeometry(x, y, width, height)
        self.setFontSize(14)
        self.setAlignment(Qt.AlignVCenter)

    def setFontSize(self, size):
        font = QFont()
        font.setPixelSize(size)
        self.setFont(font)

    def setBackground(self, image_name):
        self.setStyleSheet(self.styleSheet()+"border-image:url(RESOURCE/drawable/" + image_name +");")

    def setBackgroundColor(self, color):
        self.setStyleSheet(self.styleSheet()+"background-color:"+color+";")

    def setTextColor(self, color):
        self.setStyleSheet(self.styleSheet()+"color:"+color+";")

    def setDisplayMode(self, displayMode):
        if displayMode == PyQt5_QLineEdit.Password:
            self.setEchoMode(displayMode)
        elif displayMode == PyQt5_QLineEdit.Normal:
            self.setEchoMode(displayMode)
        elif displayMode == PyQt5_QLineEdit.NoEcho:
            self.setEchoMode(displayMode)
        elif displayMode == PyQt5_QLineEdit.PasswordEchoOnEdit:
            self.setEchoMode(displayMode)

# 创建标签label
class PyQt5_Qlabel(QLabel):
    clicked=pyqtSignal(QMouseEvent)
    def __init__(self, QWidget, x =0, y = 0, width = 60, height = 16):
        super().__init__(QWidget)
        self.widget=QWidget
        self.zeze=True
        self.setGeometry(x, y, width, height)
    def setFontSize(self, size):
        font = QFont()
        font.setPixelSize(size)
        self.setFont(font)
    def setFontFitSize(self, size):
        font = QFont()
        font.setPointSize(size)
        self.setFont(font)
    def setBackground(self, image_name):
        self.setStyleSheet(self.styleSheet()+"border-image:url(RESOURCE/drawable/" + image_name +");")

    def setBackgroundColor(self, color):
        self.setStyleSheet(self.styleSheet()+"background-color:"+color+";")

    def setTextColor(self, color):
        self.setStyleSheet(self.styleSheet()+"color:"+color+";")
    def mouseReleaseEvent(self, e):
        self.released.emit(e)
    released = pyqtSignal(QMouseEvent)
    pressed = pyqtSignal(QEvent)
    def mousePressEvent(self, event): 
        self.pressed.emit(event)
        if event.buttons() == Qt.LeftButton:     
            self.clicked.emit(event)
    moved= pyqtSignal(QMouseEvent)
    def mouseMoveEvent(self, event):
        self.moved.emit(event)
    doubleclicked = pyqtSignal(QMouseEvent)
    def mouseDoubleClickEvent(self, event): 
        if event.buttons() == Qt.LeftButton:    
            self.doubleclicked.emit(event)
    entered = pyqtSignal(QEnterEvent)
    def enterEvent(self,event):
        self.entered.emit(event)

    leaved = pyqtSignal(QEvent)
    def leaveEvent(self,event):
        self.leaved.emit(event)

    
    def setSize(self,x):
        self.setFixedSize(x)
    def refresh(self):
        if self.zeze:
            self.widget.resize(self.widget.width()+1,self.widget.height()+1)
            self.zeze=False
        else :
            self.widget.resize(self.widget.width()-1,self.widget.height()-1)
            self.zeze=True

class PyQt5_QMovie(QMovie):
    def __init__(self, name):
        super().__init__("RESOURCE/gif/"+ name)

class PyQt5_QMediaPlayer():
    def __init__(self):
        pygame.mixer.init()
        self.music = pygame.mixer.music
    def prepare_audio(self, file_name):
        self.music.load("RESOURCE/audio/" + file_name)
    def prepare_voice(self, file_name):
        self.music.load("RESOURCE/voice/" + file_name)
    def play(self, loops=1, start=0.0):
        if loops == 0:
            self.music.play(-1, start)
        elif loops < 0:
            pass
        elif loops > 0:
            self.music.play(loops - 1, start)
    def stop(self):
        self.music.stop()
    def pause(self):
        self.music.pause()
    def setVolume(self, value):
        self.music.set_volume(value)
    def isPlaying(self):
        if self.music.get_busy() == 1:
            return True
        else: 
            return False


# 创建复选框checkBox
class PyQt5_QCheckBox(QCheckBox):
    def __init__(self, QWidget, x =0, y = 0, width = 20, height = 20):
        super().__init__(QWidget)
        self.setGeometry(x, y, width, height)
        self.isIndicator = True
        self.image_name_normal = ""
        self.image_name_pressed = ""

    def setIndicator(self, isIndicator):
        self.isIndicator = isIndicator
        self.setStyleSheet("")
        if self.image_name_normal != "":
            self.setUncheckedBackground(self.image_name_normal)
        if self.image_name_pressed != "":
            self.setCheckedBackground(self.image_name_pressed)

    def setUncheckedBackground(self, image_name):
        if self.isIndicator:
            self.setStyleSheet(self.styleSheet()+"QCheckBox:unchecked{width:"+str(self.width())
                +"px;height:"+str(self.height())+"px;border-image:url(RESOURCE/drawable/"
                +image_name+")}")
        else:
            self.setStyleSheet(self.styleSheet()+"QCheckBox:indicator:unchecked{width:"
            +str(self.width())+"px;height:"+str(self.height())+
            "px;border-image:url(RESOURCE/drawable/"+image_name+")}")
        self.image_name_normal = image_name
    
    def setCheckedBackground(self, image_name):
        if self.isIndicator:
            self.setStyleSheet(self.styleSheet()+"QCheckBox:checked{width:"+str(self.width())
                +"px;height:"+str(self.height())+"px;border-image:url(RESOURCE/drawable/"
                +image_name+")}")
        else:
            self.setStyleSheet(self.styleSheet()+"QCheckBox:indicator:checked{width:"
            +str(self.width())+"px;height:"+str(self.height())+"px;border-image:url(RESOURCE/drawable/"
            +image_name+")}")
        self.image_name_pressed = image_name

# 创建单选钮radioButton
class PyQt5_QRadioButton(QRadioButton):
    def __init__(self, QWidget, x =0, y = 0, width = 20, height = 20):
        super().__init__(QWidget)
        self.setGeometry(x, y, width, height)
        self.isIndicator = True
        self.image_name_normal = ""
        self.image_name_pressed = ""

    def setFontSize(self, size):
        font = QFont()
        font.setPixelSize(size)
        self.setFont(font)
        
    def setTextColor(self, color):
        self.setStyleSheet(self.styleSheet()+"color:"+color+";")

    def setIndicator(self, isIndicator):
        self.isIndicator = isIndicator
        self.setStyleSheet("")
        if self.image_name_normal != "":
            self.setUncheckedBackground(self.image_name_normal)
        if self.image_name_pressed != "":
            self.setCheckedBackground(self.image_name_pressed)

    def setUncheckedBackground(self, image_name):
        if self.isIndicator:
            self.setStyleSheet(self.styleSheet()+"QRadioButton:unchecked{width:"+str(self.width())
                +"px;height:"+str(self.height())+"px;border-image:url(RESOURCE/drawable/"
                +image_name+")}")
        else:
            self.setStyleSheet(self.styleSheet()+"QRadioButton:indicator:unchecked{width:"
            +str(self.width())+"px;height:"+str(self.height())+
            "px;border-image:url(RESOURCE/drawable/"+image_name+")}")
        self.image_name_normal = image_name
    
    def setCheckedBackground(self, image_name):
        if self.isIndicator:
            self.setStyleSheet(self.styleSheet()+"QRadioButton:checked{width:"+str(self.width())
                +"px;height:"+str(self.height())+"px;border-image:url(RESOURCE/drawable/"
                +image_name+")}")
        else:
            self.setStyleSheet(self.styleSheet()+"QRadioButton:indicator:checked{width:"
            +str(self.width())+"px;height:"+str(self.height())+"px;border-image:url(RESOURCE/drawable/"
            +image_name+")}")
        self.image_name_pressed = image_name

# 创建一个组GroupBox
class PyQt5_QGroupBox(QGroupBox):
    def __init__(self, QWidget, x =0, y = 0, width = 120, height = 80):
        super().__init__(QWidget)
        self.setGeometry(x, y, width, height)
        self.setObjectName("groupbox")
    
    def setBackground(self, image_name):
        self.setStyleSheet("#groupbox{border-image:url(RESOURCE/drawable/"+image_name+")}")

    def setBackgroundColor(self, color):
        self.setStyleSheet("#groupbox{background-color:"+color+"}")
    
    def setBorderWidth(self,width):
        self.setStyleSheet(self.styleSheet()+"border-width:"+str(width)+"px;border-style:solid;")


def getQuestion(id):
    try:
        # 题库的地址
        request = ipStr+'ti/findById.do?id=%d'%id
        request = urllib.request.Request(url=request)
        request.add_header('Content-Type','application/json')
        conn = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        info = {"id":1,"wenti":"由于网络问题未找到所需内容，请检查您的网络","daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}
        return info
    # 获得网上数据
    info = json.loads(conn.read().decode('utf-8'))
    # 获得字典 问题详情 
    if info:
        if info["state"] != 0:
            return {"id":1,"wenti":info["message"],"daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}
        else:
            return info["data"]
def reductionRadioBtn(optionsBtn):
    for x in range(len(optionsBtn)):
        optionsBtn[x].setCheckable(False)
        optionsBtn[x].setCheckable(True)    
class PyQt5_QSystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(PyQt5_QSystemTrayIcon, self).__init__(parent)
        self.menu = QMenu()
        self.setContextMenu(self.menu)
    def addMenu(self,name):
        self.menuAction = QAction(name,self)
        self.menu.addAction(self.menuAction)
        return self.menuAction
    def _setIcon(self, icon_name):
        self.setIcon(QIcon("RESOURCE/drawable/" + icon_name )) 


class PyQt5_Animation(QPropertyAnimation):
    animFinished = pyqtSignal()
    def __init__(self,QWidget=None):
        super(PyQt5_Animation,self).__init__()
        self.setPropertyName(b"geometry")
        self.setTargetObject(QWidget) 
        self.finished.connect(self.aFinished)
        self.widget=QWidget
        self.valueChanged.connect(self.up)
        self.ze=True
    def up(self):
        if self.ze:
            self.widget.resize(self.widget.width()+1,self.widget.height()+1)
            self.ze=False
        else:
            self.widget.resize(self.widget.width()-1,self.widget.height()-1)
            self.ze=True
        
    def setStartValues(self,x,y,z,i):
        self.setStartValue(QRect(x,y,z,i))
    def setEndValues(self,x,y,z,i):
        self.setEndValue(QRect(x,y,z,i))
    def setMode(self,Mode):
        self.setEasingCurve(Mode)
    def aFinished(self):
        self.animFinished.emit()

class Mode():

    InOut=QEasingCurve.InOutBack
    OutIn=QEasingCurve.OutInBack

    InZero=QEasingCurve.InQuart
    OutZero= QEasingCurve.OutQuart

    InElastic=QEasingCurve.InElastic
    OutElastic = QEasingCurve.OutElastic

    InBounce = QEasingCurve.InBounce
    OutBounce = QEasingCurve.OutBounce
# 创建透明窗口
class PyQt5_FramelessBox(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(340,340)
        self.setObjectName("FramelessBox")
        self.setWindowFlags(self.windowFlags()|Qt.FramelessWindowHint)

    def setWindowsTop(self,flag):
        if flag:
            self.setWindowFlags(self.windowFlags()|Qt.WindowStaysOnTopHint)
    def setResize(self, width, height):
        self.resize(width, height)
    def setWindowsTransparent(self,flag):
        if flag: 
            self.setAttribute(Qt.WA_TranslucentBackground, True) 

def getDesktopWidth():
    return QApplication.desktop().width()

def getDesktopHeight():
    return QApplication.desktop().height()

def rock(dialog,num):
    global angle,direction
    num1 = num*math.sin(angle)
    num2 = num*math.cos(angle)
    if direction == 1:
        if angle<=1:
            angle += 0.15
        else:
            direction = -1
    if direction == -1:
        if angle >= -1:
            angle -= 0.15
        else:
            direction = 1     
    dialog.finalX = num1
    dialog.finalY = num2

def refresh(dialog,t):
    for i in range(t):  
        dialog.update()
        time.sleep(0.01) 

def judge(dialog,x,y,type1,type2,type3,s1,s2,s3):
    global flg,fff,f,border,borderr
    if f == 1:  
        flg = 1
    for i in range(len(dialog.listXY)): 
        if dialog.namelist[i][1] == type1:
            border = s1
        elif dialog.namelist[i][1] == type2:
            border = s2
        elif dialog.namelist[i][1] == type3:
            border = s3
        if x >= dialog.listXY[i][0]-5 and x<= dialog.listXY[i][0] + border + 5:
            if y >= dialog.listXY[i][1] and y <= dialog.listXY[i][1] + border:
                borderr = border
                dialog.index = i
                print("碰到了")
                flg = 1
    if dialog.distanceY>300: 
        fff = 1
        flg = 1

def lengths(dialog,num):
    dialog.distanceY += num
    dialog.distanceX += (num*dialog.finalX)/dialog.finalY

def YesOrNo(dialog):
    global flg,fff,f
    if flg != 1 and dialog.distanceY>=0 and dialog.distanceY<= 300:    # 绳子向下
        lengths(dialog,2)   
        dialog.hook.move(290+dialog.finalX+dialog.distanceX, 58+dialog.finalY+dialog.distanceY)
        return 0,0
    elif flg==1 and dialog.distanceY>=0 and fff != 1:   # 吊到了
        f = 1
        lengths(dialog,-2) 
        return 1,0 
    elif flg == 1 and fff == 1 and dialog.distanceY>=0:  
        f = 1
        lengths(dialog,-2) 
        dialog.hook.move(290+dialog.finalX+dialog.distanceX, 58+dialog.finalY+dialog.distanceY)
        return 0,0
    else:
        if fff != 1:
            dialog.distanceY = 0 
            flg,f,fff,dialog.isdo = 0,0,0,0
            return 1,1
        dialog.distanceY = 0 
        flg,f,fff,dialog.isdo = 0,0,0,0
        return 0,0
    
def playAudio(auido_name):
    music = PyQt5_QMediaPlayer()
    music.prepare_audio(auido_name)
    music.play()

def change_img(dialog,goldReward,diamondReward,stoneReward):
    if dialog.namelist[dialog.index][1] == goldReward:
        dialog.namelist[dialog.index][0].setBackground("hook_gold.png")
    elif dialog.namelist[dialog.index][1] == diamondReward:
        dialog.namelist[dialog.index][0].setBackground("hook_diamond.png")
    else:
        dialog.namelist[dialog.index][0].setBackground("hook_stone.png")

def getBorder():
    return borderr
        

name="Vipc2"