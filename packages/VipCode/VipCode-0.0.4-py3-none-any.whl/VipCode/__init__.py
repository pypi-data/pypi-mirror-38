from PyQt5 .QtCore import *#line:1
from PyQt5 .QtGui import *#line:2
from PyQt5 .QtWidgets import *#line:3
import sys #line:4
import os #line:5
import json #line:6
import pygame #line:7
import time #line:8
import urllib #line:9
import random #line:10
import math #line:11
parwidth =600 #line:13
flg =0 #line:15
fff =0 #line:16
f =0 #line:17
border =0 #line:18
borderr =0 #line:19
angle =1 #line:20
direction =1 #line:21
ipStr ='http://jiaoxue.vipcode.cn/'#line:23
global filename #line:25
filename =""#line:26
class PyQt5_QDialog (QDialog ):#line:29
    def __init__ (O0O0O0000000OOO00 ):#line:30
        super ().__init__ ()#line:31
        O0O0O0000000OOO00 .setObjectName ("dialog")#line:32
        global parwidth #line:33
        parwidth =O0O0O0000000OOO00 .width ()+200 #line:34
    def setBackgroundColor (O0000OO00OOOO00O0 ,OOO0000O00OO000OO ):#line:35
        O0000OO00OOOO00O0 .setStyleSheet ("#dialog{background-color:"+OOO0000O00OO000OO +"}")#line:36
    def setBackground (OO000OO00O000O00O ,OO0OO0O00O0OO0O0O ):#line:37
        OO000OO00O000O00O .setStyleSheet ("#dialog{border-image:url(RESOURCE/drawable/"+OO0OO0O00O0OO0O0O +")}")#line:38
    def setResize (O0O000OOOO00O0OOO ,O0OOOO00O00O0O0O0 ,OOO0OO00000OO0O00 ):#line:40
        O0O000OOOO00O0OOO .resize (O0OOOO00O00O0O0O0 ,OOO0OO00000OO0O00 )#line:41
    def addBodyButton (O0OO00O0OOOOO0OO0 ,OOO0O00OOO00OO000 ):#line:43
        O0OO00O0OOOOO0OO0 .bodylabel =OOO0O00OOO00OO000 #line:44
        O0OO00O0OOOOO0OO0 .head =PyQt5_QPushButton (O0OO00O0OOOOO0OO0 ,400 ,300 ,160 ,130 )#line:45
        O0OO00O0OOOOO0OO0 .head .setBackgroundColor ("rgba(100,0, 200, 0)")#line:46
        O0OO00O0OOOOO0OO0 .body =PyQt5_QPushButton (O0OO00O0OOOOO0OO0 ,445 ,430 ,70 ,80 )#line:48
        O0OO00O0OOOOO0OO0 .body .setBackgroundColor ("rgba(100,0, 200, 0)")#line:49
        O0OO00O0OOOOO0OO0 .leftArm =PyQt5_QPushButton (O0OO00O0OOOOO0OO0 ,420 ,430 ,40 ,30 )#line:51
        O0OO00O0OOOOO0OO0 .leftArm .setBackgroundColor ("rgba(0,0, 0, 0)")#line:52
        O0OO00O0OOOOO0OO0 .rightArm =PyQt5_QPushButton (O0OO00O0OOOOO0OO0 ,505 ,430 ,50 ,30 )#line:54
        O0OO00O0OOOOO0OO0 .rightArm .setBackgroundColor ("rgba(0,0, 0, 0)")#line:55
        O0OO00O0OOOOO0OO0 .leftFoot =PyQt5_QPushButton (O0OO00O0OOOOO0OO0 ,440 ,500 ,30 ,30 )#line:57
        O0OO00O0OOOOO0OO0 .leftFoot .setBackgroundColor ("rgba(0,0, 0, 0)")#line:58
        O0OO00O0OOOOO0OO0 .rightFoot =PyQt5_QPushButton (O0OO00O0OOOOO0OO0 ,500 ,500 ,30 ,30 )#line:60
        O0OO00O0OOOOO0OO0 .rightFoot .setBackgroundColor ("rgba(0,0, 0, 0)")#line:61
        O0OO00O0OOOOO0OO0 .head .clicked .connect (O0OO00O0OOOOO0OO0 .headClicked )#line:63
        O0OO00O0OOOOO0OO0 .leftArm .clicked .connect (O0OO00O0OOOOO0OO0 .armClicked )#line:64
        O0OO00O0OOOOO0OO0 .rightArm .clicked .connect (O0OO00O0OOOOO0OO0 .armClicked )#line:65
        O0OO00O0OOOOO0OO0 .rightFoot .clicked .connect (O0OO00O0OOOOO0OO0 .rightFootClicked )#line:66
        O0OO00O0OOOOO0OO0 .leftFoot .clicked .connect (O0OO00O0OOOOO0OO0 .leftFootClicked )#line:67
        O0OO00O0OOOOO0OO0 .body .clicked .connect (O0OO00O0OOOOO0OO0 .bodyClicked )#line:68
    def armClicked (OO00O00OO000O000O ):#line:69
        OO00O00OO000O000O .neibu2 ('main_arm')#line:70
        OO00O00OO000O000O .neibu1 ('main_arm')#line:75
    def leftFootClicked (OO0O00O0OOO0O00O0 ):#line:76
        OO0O00O0OOO0O00O0 .neibu2 ('main_leftFoot')#line:77
        OO0O00O0OOO0O00O0 .neibu1 ('main_leftFoot')#line:78
    def rightFootClicked (OO00OOOO000000O0O ):#line:79
        OO00OOOO000000O0O .neibu2 ('main_rightFoot')#line:80
        OO00OOOO000000O0O .neibu1 ('main_rightFoot')#line:81
    def bodyClicked (OO0OO0OO0000OO00O ):#line:82
        OO0OO0OO0000OO00O .neibu2 ('main_body')#line:83
        OO0OO0OO0000OO00O .neibu1 ('main_body')#line:84
    def headClicked (O0O0OOO000000O000 ):#line:85
        O0O0OOO000000O000 .neibu2 ('main_head')#line:86
        O0O0OOO000000O000 .neibu1 ('main_head')#line:87
    def neibu2 (OOO0000O0O0O00OOO ,OO0OOOOO0O0O00O0O ):#line:89
        OOO0000O0O0O00OOO .neigif =PyQt5_QMovie (OO0OOOOO0O0O00O0O +'.gif')#line:91
        OOO0000O0O0O00OOO .neigif .setScaledSize (OOO0000O0O0O00OOO .bodylabel .size ())#line:93
        OOO0000O0O0O00OOO .bodylabel .setMovie (OOO0000O0O0O00OOO .neigif )#line:95
        OOO0000O0O0O00OOO .neigif .start ()#line:97
        OOO0000O0O0O00OOO .frameCount =OOO0000O0O0O00OOO .neigif .frameCount ()#line:98
        OOO0000O0O0O00OOO .neigif .frameChanged .connect (OOO0000O0O0O00OOO .neibu3 )#line:100
    def neibu3 (OOO0000O0O0OOO00O ):#line:101
        OOO0000O0O0OOO00O .frameCount -=1 #line:103
        if OOO0000O0O0OOO00O .frameCount ==0 :#line:105
            OOO0000O0O0OOO00O .neigif .stop ()#line:107
            OOO0000O0O0OOO00O .neigif =PyQt5_QMovie ('main_lion.gif')#line:109
            OOO0000O0O0OOO00O .neigif .setScaledSize (OOO0000O0O0OOO00O .bodylabel .size ())#line:110
            OOO0000O0O0OOO00O .bodylabel .setMovie (OOO0000O0O0OOO00O .neigif )#line:112
            OOO0000O0O0OOO00O .neigif .start ()#line:114
    def neibu1 (OO0000OO0OOOO0OO0 ,O0O0000O0OOOO00O0 ):#line:116
        O0OOO0OOO00000O0O =PyQt5_QMediaPlayer ()#line:118
        O0OOO0OOO00000O0O .prepare_audio (O0O0000O0OOOO00O0 +'.wav')#line:120
        O0OOO0OOO00000O0O .play ()#line:122
class PyQt5_QPushButton (QPushButton ):#line:125
    def __init__ (OOO00OO0O0OO0OO00 ,OOOOO00000OO0000O ,x =0 ,y =0 ,width =113 ,height =32 ):#line:126
        super ().__init__ (OOOOO00000OO0000O )#line:127
        OOO00OO0O0OO0OO00 .setGeometry (x ,y ,width ,height )#line:128
    def setBackground (OO0O00OO0O0OOOO00 ,OOOOO0000O00O0OOO ):#line:130
        OO0O00OO0O0OOOO00 .setStyleSheet (OO0O00OO0O0OOOO00 .styleSheet ()+"QPushButton{border-image:url(RESOURCE/drawable/"+OOOOO0000O00O0OOO +")}")#line:132
    def setPressedBackground (OO0OOOOOOOO00OOOO ,O0O0000000OO000OO ):#line:134
        OO0OOOOOOOO00OOOO .setStyleSheet (OO0OOOOOOOO00OOOO .styleSheet ()+"QPushButton:pressed{border-image:url(RESOURCE/drawable/"+O0O0000000OO000OO +")}")#line:136
    def setBackgroundColor (OOO0OOOO0OOO0O0OO ,OOOOO00O0OOOO0000 ):#line:138
        OOO0OOOO0OOO0O0OO .setStyleSheet (OOO0OOOO0OOO0O0OO .styleSheet ()+"QPushButton{background-color:"+OOOOO00O0OOOO0000 +"}")#line:139
    def setTextColor (OOO00OOOOOOO0OOOO ,O0000000OOOOO0O00 ):#line:141
        OOO00OOOOOOO0OOOO .setStyleSheet (OOO00OOOOOOO0OOOO .styleSheet ()+"QPushButton{color:"+O0000000OOOOO0O00 +"}")#line:142
    def setPressedTextColor (OOO0OO0OOOOOO0OOO ,OOOO0O00OOO000O00 ):#line:144
        OOO0OO0OOOOOO0OOO .setStyleSheet (OOO0OO0OOOOOO0OOO .styleSheet ()+"QPushButton:pressed{color:"+OOOO0O00OOO000O00 +"}")#line:145
    def setFontSize (OO0OO00O0OOO0000O ,OO0O00000OO0O0O00 ):#line:147
        OO0000000OO0O00OO =QFont ()#line:148
        OO0000000OO0O00OO .setPixelSize (OO0O00000OO0O0O00 )#line:149
        OO0OO00O0OOO0000O .setFont (OO0000000OO0O00OO )#line:150
class PyQt5_QLineEdit (QLineEdit ):#line:153
    Password =QLineEdit .Password #line:154
    Normal =QLineEdit .Normal #line:155
    NoEcho =QLineEdit .NoEcho #line:156
    PasswordEchoOnEdit =QLineEdit .PasswordEchoOnEdit #line:157
    def __init__ (OOO0O00O0OO00O0OO ,O0O00O0000OOOO00O ,x =0 ,y =0 ,width =113 ,height =21 ):#line:159
        super ().__init__ (O0O00O0000OOOO00O )#line:160
        OOO0O00O0OO00O0OO .setGeometry (x ,y ,width ,height )#line:161
        OOO0O00O0OO00O0OO .setFontSize (14 )#line:162
        OOO0O00O0OO00O0OO .setAlignment (Qt .AlignVCenter )#line:163
    def setFontSize (O00O0O00OOOOO00O0 ,O0000000OO0O000O0 ):#line:165
        OO0OO000O00OOOOO0 =QFont ()#line:166
        OO0OO000O00OOOOO0 .setPixelSize (O0000000OO0O000O0 )#line:167
        O00O0O00OOOOO00O0 .setFont (OO0OO000O00OOOOO0 )#line:168
    def setBackground (O0OOO00000O00O00O ,OOO0000O0000O0000 ):#line:170
        O0OOO00000O00O00O .setStyleSheet (O0OOO00000O00O00O .styleSheet ()+"border-image:url(RESOURCE/drawable/"+OOO0000O0000O0000 +");")#line:171
    def setBackgroundColor (O00O00OO0OOO0O0OO ,O0O0O0OO0OOOO00OO ):#line:173
        O00O00OO0OOO0O0OO .setStyleSheet (O00O00OO0OOO0O0OO .styleSheet ()+"background-color:"+O0O0O0OO0OOOO00OO +";")#line:174
    def setTextColor (O00OO0O0000O000O0 ,O0000O0000OOOOO0O ):#line:176
        O00OO0O0000O000O0 .setStyleSheet (O00OO0O0000O000O0 .styleSheet ()+"color:"+O0000O0000OOOOO0O +";")#line:177
    def setDisplayMode (O00O0000000000O00 ,O0O00O0OOO0O0O000 ):#line:179
        if O0O00O0OOO0O0O000 ==PyQt5_QLineEdit .Password :#line:180
            O00O0000000000O00 .setEchoMode (O0O00O0OOO0O0O000 )#line:181
        elif O0O00O0OOO0O0O000 ==PyQt5_QLineEdit .Normal :#line:182
            O00O0000000000O00 .setEchoMode (O0O00O0OOO0O0O000 )#line:183
        elif O0O00O0OOO0O0O000 ==PyQt5_QLineEdit .NoEcho :#line:184
            O00O0000000000O00 .setEchoMode (O0O00O0OOO0O0O000 )#line:185
        elif O0O00O0OOO0O0O000 ==PyQt5_QLineEdit .PasswordEchoOnEdit :#line:186
            O00O0000000000O00 .setEchoMode (O0O00O0OOO0O0O000 )#line:187
class PyQt5_Qlabel (QLabel ):#line:190
    clicked =pyqtSignal (QMouseEvent )#line:191
    def __init__ (OO00OO0O0OO0OOO00 ,OOO0OO00O000O00O0 ,x =0 ,y =0 ,width =60 ,height =16 ):#line:192
        super ().__init__ (OOO0OO00O000O00O0 )#line:193
        OO00OO0O0OO0OOO00 .widget =OOO0OO00O000O00O0 #line:194
        OO00OO0O0OO0OOO00 .zeze =True #line:195
        OO00OO0O0OO0OOO00 .setGeometry (x ,y ,width ,height )#line:196
    def setFontSize (O0OO00OO00OO000OO ,O0OOO00000O0000OO ):#line:197
        OOO0O0O0O0O0O0O00 =QFont ()#line:198
        OOO0O0O0O0O0O0O00 .setPixelSize (O0OOO00000O0000OO )#line:199
        O0OO00OO00OO000OO .setFont (OOO0O0O0O0O0O0O00 )#line:200
    def setFontFitSize (O0OOO0OO0O0O00O0O ,OO00O0OOO0O0OO0OO ):#line:201
        OOOO0O0O0O000O000 =QFont ()#line:202
        OOOO0O0O0O000O000 .setPointSize (OO00O0OOO0O0OO0OO )#line:203
        O0OOO0OO0O0O00O0O .setFont (OOOO0O0O0O000O000 )#line:204
    def setBackground (OO0OO000OOO00O0O0 ,OO0OOOO0O00O0OOOO ):#line:205
        OO0OO000OOO00O0O0 .setStyleSheet (OO0OO000OOO00O0O0 .styleSheet ()+"border-image:url(RESOURCE/drawable/"+OO0OOOO0O00O0OOOO +");")#line:206
    def setBackgroundColor (OO00OO00OOOO0000O ,O00000O0OO0O000O0 ):#line:208
        OO00OO00OOOO0000O .setStyleSheet (OO00OO00OOOO0000O .styleSheet ()+"background-color:"+O00000O0OO0O000O0 +";")#line:209
    def setTextColor (OO00OOO000O0O0O0O ,OO0O00OOO0O0OO0OO ):#line:211
        OO00OOO000O0O0O0O .setStyleSheet (OO00OOO000O0O0O0O .styleSheet ()+"color:"+OO0O00OOO0O0OO0OO +";")#line:212
    def mouseReleaseEvent (OOO00OO0O0O00OO0O ,O0O00000OO0OOOO00 ):#line:213
        OOO00OO0O0O00OO0O .released .emit (O0O00000OO0OOOO00 )#line:214
    released =pyqtSignal (QMouseEvent )#line:215
    pressed =pyqtSignal (QEvent )#line:216
    def mousePressEvent (O0000000O00O0OOO0 ,O000000000O0OOO00 ):#line:217
        O0000000O00O0OOO0 .pressed .emit (O000000000O0OOO00 )#line:218
        if O000000000O0OOO00 .buttons ()==Qt .LeftButton :#line:219
            O0000000O00O0OOO0 .clicked .emit (O000000000O0OOO00 )#line:220
    moved =pyqtSignal (QMouseEvent )#line:221
    def mouseMoveEvent (OOOOOOOO0OO00O0OO ,O0O0O000O0O0OO000 ):#line:222
        OOOOOOOO0OO00O0OO .moved .emit (O0O0O000O0O0OO000 )#line:223
    doubleclicked =pyqtSignal (QMouseEvent )#line:224
    def mouseDoubleClickEvent (O0OOOOOO00OOO0OO0 ,O00OOO000000OOO00 ):#line:225
        if O00OOO000000OOO00 .buttons ()==Qt .LeftButton :#line:226
            O0OOOOOO00OOO0OO0 .doubleclicked .emit (O00OOO000000OOO00 )#line:227
    entered =pyqtSignal (QEnterEvent )#line:228
    def enterEvent (OOO00OOO0O0OO0OOO ,OO0OOO00O00000OO0 ):#line:229
        OOO00OOO0O0OO0OOO .entered .emit (OO0OOO00O00000OO0 )#line:230
    leaved =pyqtSignal (QEvent )#line:232
    def leaveEvent (OO0OOO0000OO0O000 ,O0000OOOO0O00OO0O ):#line:233
        OO0OOO0000OO0O000 .leaved .emit (O0000OOOO0O00OO0O )#line:234
    def setSize (OO0OO0O00O0000OO0 ,OO0O0OOO0O000O0O0 ):#line:237
        OO0OO0O00O0000OO0 .setFixedSize (OO0O0OOO0O000O0O0 )#line:238
    def refresh (OO0OO0000O000OOO0 ):#line:239
        if OO0OO0000O000OOO0 .zeze :#line:240
            OO0OO0000O000OOO0 .widget .resize (OO0OO0000O000OOO0 .widget .width ()+1 ,OO0OO0000O000OOO0 .widget .height ()+1 )#line:241
            OO0OO0000O000OOO0 .zeze =False #line:242
        else :#line:243
            OO0OO0000O000OOO0 .widget .resize (OO0OO0000O000OOO0 .widget .width ()-1 ,OO0OO0000O000OOO0 .widget .height ()-1 )#line:244
            OO0OO0000O000OOO0 .zeze =True #line:245
class PyQt5_QMovie (QMovie ):#line:247
    def __init__ (O00OO0OOOOOOO000O ,O0O0O0O0000O0OOOO ):#line:248
        super ().__init__ ("RESOURCE/gif/"+O0O0O0O0000O0OOOO )#line:249
class PyQt5_QMediaPlayer ():#line:251
    def __init__ (O00O000OO00O0O0OO ):#line:252
        pygame .mixer .init ()#line:253
        O00O000OO00O0O0OO .music =pygame .mixer .music #line:254
    def prepare_audio (O000O00O000OO0000 ,OO00000O0OO0O00OO ):#line:255
        O000O00O000OO0000 .music .load ("RESOURCE/audio/"+OO00000O0OO0O00OO )#line:256
    def prepare_voice (OO000000OOO00OOOO ,O0O0OO00O0O00OOOO ):#line:257
        OO000000OOO00OOOO .music .load ("RESOURCE/voice/"+O0O0OO00O0O00OOOO )#line:258
    def play (OO00OO00OO0O0OO00 ,loops =1 ,start =0.0 ):#line:259
        if loops ==0 :#line:260
            OO00OO00OO0O0OO00 .music .play (-1 ,start )#line:261
        elif loops <0 :#line:262
            pass #line:263
        elif loops >0 :#line:264
            OO00OO00OO0O0OO00 .music .play (loops -1 ,start )#line:265
    def stop (O000O00O0OO0O0O0O ):#line:266
        O000O00O0OO0O0O0O .music .stop ()#line:267
    def pause (O0000O0OOOOO0O00O ):#line:268
        O0000O0OOOOO0O00O .music .pause ()#line:269
    def setVolume (O0OOOO00000O0O000 ,OOO0O0OOOOOO00OOO ):#line:270
        O0OOOO00000O0O000 .music .set_volume (OOO0O0OOOOOO00OOO )#line:271
    def isPlaying (O000OOOO000O00000 ):#line:272
        if O000OOOO000O00000 .music .get_busy ()==1 :#line:273
            return True #line:274
        else :#line:275
            return False #line:276
class PyQt5_QCheckBox (QCheckBox ):#line:280
    def __init__ (O0O0O0O0000OOO000 ,OO00OO0OOOO0OOOO0 ,x =0 ,y =0 ,width =20 ,height =20 ):#line:281
        super ().__init__ (OO00OO0OOOO0OOOO0 )#line:282
        O0O0O0O0000OOO000 .setGeometry (x ,y ,width ,height )#line:283
        O0O0O0O0000OOO000 .isIndicator =True #line:284
        O0O0O0O0000OOO000 .image_name_normal =""#line:285
        O0O0O0O0000OOO000 .image_name_pressed =""#line:286
    def setIndicator (O0O0O0O00O00O00O0 ,O00OO0OOO0OO0OOOO ):#line:288
        O0O0O0O00O00O00O0 .isIndicator =O00OO0OOO0OO0OOOO #line:289
        O0O0O0O00O00O00O0 .setStyleSheet ("")#line:290
        if O0O0O0O00O00O00O0 .image_name_normal !="":#line:291
            O0O0O0O00O00O00O0 .setUncheckedBackground (O0O0O0O00O00O00O0 .image_name_normal )#line:292
        if O0O0O0O00O00O00O0 .image_name_pressed !="":#line:293
            O0O0O0O00O00O00O0 .setCheckedBackground (O0O0O0O00O00O00O0 .image_name_pressed )#line:294
    def setUncheckedBackground (OOO00O00OOO00OO0O ,OOO0O0OO00OO000OO ):#line:296
        if OOO00O00OOO00OO0O .isIndicator :#line:297
            OOO00O00OOO00OO0O .setStyleSheet (OOO00O00OOO00OO0O .styleSheet ()+"QCheckBox:unchecked{width:"+str (OOO00O00OOO00OO0O .width ())+"px;height:"+str (OOO00O00OOO00OO0O .height ())+"px;border-image:url(RESOURCE/drawable/"+OOO0O0OO00OO000OO +")}")#line:300
        else :#line:301
            OOO00O00OOO00OO0O .setStyleSheet (OOO00O00OOO00OO0O .styleSheet ()+"QCheckBox:indicator:unchecked{width:"+str (OOO00O00OOO00OO0O .width ())+"px;height:"+str (OOO00O00OOO00OO0O .height ())+"px;border-image:url(RESOURCE/drawable/"+OOO0O0OO00OO000OO +")}")#line:304
        OOO00O00OOO00OO0O .image_name_normal =OOO0O0OO00OO000OO #line:305
    def setCheckedBackground (O0OOO0OOO0OO00000 ,OOO00O000O0OOOOOO ):#line:307
        if O0OOO0OOO0OO00000 .isIndicator :#line:308
            O0OOO0OOO0OO00000 .setStyleSheet (O0OOO0OOO0OO00000 .styleSheet ()+"QCheckBox:checked{width:"+str (O0OOO0OOO0OO00000 .width ())+"px;height:"+str (O0OOO0OOO0OO00000 .height ())+"px;border-image:url(RESOURCE/drawable/"+OOO00O000O0OOOOOO +")}")#line:311
        else :#line:312
            O0OOO0OOO0OO00000 .setStyleSheet (O0OOO0OOO0OO00000 .styleSheet ()+"QCheckBox:indicator:checked{width:"+str (O0OOO0OOO0OO00000 .width ())+"px;height:"+str (O0OOO0OOO0OO00000 .height ())+"px;border-image:url(RESOURCE/drawable/"+OOO00O000O0OOOOOO +")}")#line:315
        O0OOO0OOO0OO00000 .image_name_pressed =OOO00O000O0OOOOOO #line:316
class PyQt5_QRadioButton (QRadioButton ):#line:319
    def __init__ (OO0OO0OOO00OOOOO0 ,O0000O00O0O000OO0 ,x =0 ,y =0 ,width =20 ,height =20 ):#line:320
        super ().__init__ (O0000O00O0O000OO0 )#line:321
        OO0OO0OOO00OOOOO0 .setGeometry (x ,y ,width ,height )#line:322
        OO0OO0OOO00OOOOO0 .isIndicator =True #line:323
        OO0OO0OOO00OOOOO0 .image_name_normal =""#line:324
        OO0OO0OOO00OOOOO0 .image_name_pressed =""#line:325
    def setFontSize (O0O0OOOO00OOOO000 ,OOOOO0OO0OO0O0O00 ):#line:327
        OOO0O0O0OOOO0OOOO =QFont ()#line:328
        OOO0O0O0OOOO0OOOO .setPixelSize (OOOOO0OO0OO0O0O00 )#line:329
        O0O0OOOO00OOOO000 .setFont (OOO0O0O0OOOO0OOOO )#line:330
    def setTextColor (O0OO00000O0OO00OO ,OO0O00O0000OO0O00 ):#line:332
        O0OO00000O0OO00OO .setStyleSheet (O0OO00000O0OO00OO .styleSheet ()+"color:"+OO0O00O0000OO0O00 +";")#line:333
    def setIndicator (OO00O00OO0OOO0000 ,O000O0000OOO00O00 ):#line:335
        OO00O00OO0OOO0000 .isIndicator =O000O0000OOO00O00 #line:336
        OO00O00OO0OOO0000 .setStyleSheet ("")#line:337
        if OO00O00OO0OOO0000 .image_name_normal !="":#line:338
            OO00O00OO0OOO0000 .setUncheckedBackground (OO00O00OO0OOO0000 .image_name_normal )#line:339
        if OO00O00OO0OOO0000 .image_name_pressed !="":#line:340
            OO00O00OO0OOO0000 .setCheckedBackground (OO00O00OO0OOO0000 .image_name_pressed )#line:341
    def setUncheckedBackground (O000O00OO0OO00000 ,OO0O0O0OOOO0O00OO ):#line:343
        if O000O00OO0OO00000 .isIndicator :#line:344
            O000O00OO0OO00000 .setStyleSheet (O000O00OO0OO00000 .styleSheet ()+"QRadioButton:unchecked{width:"+str (O000O00OO0OO00000 .width ())+"px;height:"+str (O000O00OO0OO00000 .height ())+"px;border-image:url(RESOURCE/drawable/"+OO0O0O0OOOO0O00OO +")}")#line:347
        else :#line:348
            O000O00OO0OO00000 .setStyleSheet (O000O00OO0OO00000 .styleSheet ()+"QRadioButton:indicator:unchecked{width:"+str (O000O00OO0OO00000 .width ())+"px;height:"+str (O000O00OO0OO00000 .height ())+"px;border-image:url(RESOURCE/drawable/"+OO0O0O0OOOO0O00OO +")}")#line:351
        O000O00OO0OO00000 .image_name_normal =OO0O0O0OOOO0O00OO #line:352
    def setCheckedBackground (OOO0OO00000O00O00 ,O0OO00OOOO0000O0O ):#line:354
        if OOO0OO00000O00O00 .isIndicator :#line:355
            OOO0OO00000O00O00 .setStyleSheet (OOO0OO00000O00O00 .styleSheet ()+"QRadioButton:checked{width:"+str (OOO0OO00000O00O00 .width ())+"px;height:"+str (OOO0OO00000O00O00 .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OO00OOOO0000O0O +")}")#line:358
        else :#line:359
            OOO0OO00000O00O00 .setStyleSheet (OOO0OO00000O00O00 .styleSheet ()+"QRadioButton:indicator:checked{width:"+str (OOO0OO00000O00O00 .width ())+"px;height:"+str (OOO0OO00000O00O00 .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OO00OOOO0000O0O +")}")#line:362
        OOO0OO00000O00O00 .image_name_pressed =O0OO00OOOO0000O0O #line:363
class PyQt5_QGroupBox (QGroupBox ):#line:366
    def __init__ (OOO00000OOO0O0OO0 ,OO0O0O0OO00000000 ,x =0 ,y =0 ,width =120 ,height =80 ):#line:367
        super ().__init__ (OO0O0O0OO00000000 )#line:368
        OOO00000OOO0O0OO0 .setGeometry (x ,y ,width ,height )#line:369
        OOO00000OOO0O0OO0 .setObjectName ("groupbox")#line:370
    def setBackground (OO00000O0000OO0OO ,OO00000OO00O0OO0O ):#line:372
        OO00000O0000OO0OO .setStyleSheet ("#groupbox{border-image:url(RESOURCE/drawable/"+OO00000OO00O0OO0O +")}")#line:373
    def setBackgroundColor (OO0O0OO0O0O0000OO ,OOO0O0O0OOO00O000 ):#line:375
        OO0O0OO0O0O0000OO .setStyleSheet ("#groupbox{background-color:"+OOO0O0O0OOO00O000 +"}")#line:376
    def setBorderWidth (O0O00O0OO000O0O00 ,OOOOO000OO000000O ):#line:378
        O0O00O0OO000O0O00 .setStyleSheet (O0O00O0OO000O0O00 .styleSheet ()+"border-width:"+str (OOOOO000OO000000O )+"px;border-style:solid;")#line:379
def getQuestion (O0O0000OOO0OOOOOO ):#line:382
    try :#line:383
        O000OOOO0OOO0O00O =ipStr +'ti/findById.do?id=%d'%O0O0000OOO0OOOOOO #line:385
        O000OOOO0OOO0O00O =urllib .request .Request (url =O000OOOO0OOO0O00O )#line:386
        O000OOOO0OOO0O00O .add_header ('Content-Type','application/json')#line:387
        O00OO0O000000O0OO =urllib .request .urlopen (O000OOOO0OOO0O00O )#line:388
    except urllib .error .URLError as OOOOOO000OO0000OO :#line:389
        OOO000000000OOO0O ={"id":1 ,"wenti":"由于网络问题未找到所需内容，请检查您的网络","daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:390
        return OOO000000000OOO0O #line:391
    OOO000000000OOO0O =json .loads (O00OO0O000000O0OO .read ().decode ('utf-8'))#line:393
    if OOO000000000OOO0O :#line:395
        if OOO000000000OOO0O ["state"]!=0 :#line:396
            return {"id":1 ,"wenti":OOO000000000OOO0O ["message"],"daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:397
        else :#line:398
            return OOO000000000OOO0O ["data"]#line:399
def reductionRadioBtn (OOO00O00000000O0O ):#line:400
    for OO00OOO00OOOO00OO in range (len (OOO00O00000000O0O )):#line:401
        OOO00O00000000O0O [OO00OOO00OOOO00OO ].setCheckable (False )#line:402
        OOO00O00000000O0O [OO00OOO00OOOO00OO ].setCheckable (True )#line:403
class PyQt5_QSystemTrayIcon (QSystemTrayIcon ):#line:404
    def __init__ (O0O0000O00O0OOOOO ,parent =None ):#line:405
        super (PyQt5_QSystemTrayIcon ,O0O0000O00O0OOOOO ).__init__ (parent )#line:406
        O0O0000O00O0OOOOO .menu =QMenu ()#line:407
        O0O0000O00O0OOOOO .setContextMenu (O0O0000O00O0OOOOO .menu )#line:408
    def addMenu (O00OOO0OO00O00O00 ,OOOO0OO0O0OO00OOO ):#line:409
        O00OOO0OO00O00O00 .menuAction =QAction (OOOO0OO0O0OO00OOO ,O00OOO0OO00O00O00 )#line:410
        O00OOO0OO00O00O00 .menu .addAction (O00OOO0OO00O00O00 .menuAction )#line:411
        return O00OOO0OO00O00O00 .menuAction #line:412
    def _setIcon (OO000OO0000O0O00O ,OO0O0000OOOO000OO ):#line:413
        OO000OO0000O0O00O .setIcon (QIcon ("RESOURCE/drawable/"+OO0O0000OOOO000OO ))#line:414
class PyQt5_Animation (QPropertyAnimation ):#line:417
    animFinished =pyqtSignal ()#line:418
    def __init__ (OO0O0OOOOO00OO000 ,QWidget =None ):#line:419
        super (PyQt5_Animation ,OO0O0OOOOO00OO000 ).__init__ ()#line:420
        OO0O0OOOOO00OO000 .setPropertyName (b"geometry")#line:421
        OO0O0OOOOO00OO000 .setTargetObject (QWidget )#line:422
        OO0O0OOOOO00OO000 .finished .connect (OO0O0OOOOO00OO000 .aFinished )#line:423
        OO0O0OOOOO00OO000 .widget =QWidget #line:424
        OO0O0OOOOO00OO000 .valueChanged .connect (OO0O0OOOOO00OO000 .up )#line:425
        OO0O0OOOOO00OO000 .ze =True #line:426
    def up (O00O0OO0OOOO00OO0 ):#line:427
        if O00O0OO0OOOO00OO0 .ze :#line:428
            O00O0OO0OOOO00OO0 .widget .resize (O00O0OO0OOOO00OO0 .widget .width ()+1 ,O00O0OO0OOOO00OO0 .widget .height ()+1 )#line:429
            O00O0OO0OOOO00OO0 .ze =False #line:430
        else :#line:431
            O00O0OO0OOOO00OO0 .widget .resize (O00O0OO0OOOO00OO0 .widget .width ()-1 ,O00O0OO0OOOO00OO0 .widget .height ()-1 )#line:432
            O00O0OO0OOOO00OO0 .ze =True #line:433
    def setStartValues (OOOOOOO0OO00OO000 ,O0O0OOOO0O00O0OO0 ,O0000O0O0OOOOOO00 ,OO00O0O000O0OOOO0 ,OOO0OO0OOO000OO00 ):#line:435
        OOOOOOO0OO00OO000 .setStartValue (QRect (O0O0OOOO0O00O0OO0 ,O0000O0O0OOOOOO00 ,OO00O0O000O0OOOO0 ,OOO0OO0OOO000OO00 ))#line:436
    def setEndValues (O0000O0OOOO00OOOO ,O0OO0OO00OO00O0OO ,OO0O00O00O0O00O0O ,OOOO0000000O00OO0 ,OO0000000O000OO00 ):#line:437
        O0000O0OOOO00OOOO .setEndValue (QRect (O0OO0OO00OO00O0OO ,OO0O00O00O0O00O0O ,OOOO0000000O00OO0 ,OO0000000O000OO00 ))#line:438
    def setMode (O0OOO00O0000O0O00 ,O00O00O0O0OOO000O ):#line:439
        O0OOO00O0000O0O00 .setEasingCurve (O00O00O0O0OOO000O )#line:440
    def aFinished (O0O0000O00OO00OO0 ):#line:441
        O0O0000O00OO00OO0 .animFinished .emit ()#line:442
class Mode ():#line:444
    InOut =QEasingCurve .InOutBack #line:446
    OutIn =QEasingCurve .OutInBack #line:447
    InZero =QEasingCurve .InQuart #line:449
    OutZero =QEasingCurve .OutQuart #line:450
    InElastic =QEasingCurve .InElastic #line:452
    OutElastic =QEasingCurve .OutElastic #line:453
    InBounce =QEasingCurve .InBounce #line:455
    OutBounce =QEasingCurve .OutBounce #line:456
class PyQt5_FramelessBox (QDialog ):#line:458
    def __init__ (OO00O00OO0O0OOO0O ):#line:459
        super ().__init__ ()#line:460
        OO00O00OO0O0OOO0O .resize (340 ,340 )#line:461
        OO00O00OO0O0OOO0O .setObjectName ("FramelessBox")#line:462
        OO00O00OO0O0OOO0O .setWindowFlags (OO00O00OO0O0OOO0O .windowFlags ()|Qt .FramelessWindowHint )#line:463
    def setWindowsTop (OO0OO0O000O00OO0O ,OOOO00O0OOOOOO00O ):#line:465
        if OOOO00O0OOOOOO00O :#line:466
            OO0OO0O000O00OO0O .setWindowFlags (OO0OO0O000O00OO0O .windowFlags ()|Qt .WindowStaysOnTopHint )#line:467
    def setResize (O000O0OOO00O0O000 ,OOOOOOO00OOOOOOO0 ,OOO0O0OO00OO000O0 ):#line:468
        O000O0OOO00O0O000 .resize (OOOOOOO00OOOOOOO0 ,OOO0O0OO00OO000O0 )#line:469
    def setWindowsTransparent (OO0OO0O00O00OOOO0 ,O00O0OOO000OOOO0O ):#line:470
        if O00O0OOO000OOOO0O :#line:471
            OO0OO0O00O00OOOO0 .setAttribute (Qt .WA_TranslucentBackground ,True )#line:472
def getDesktopWidth ():#line:474
    return QApplication .desktop ().width ()#line:475
def getDesktopHeight ():#line:477
    return QApplication .desktop ().height ()#line:478
def rock (OO0O0000O0O0OO0OO ,O00000000O00O0OOO ):#line:480
    global angle ,direction #line:481
    O00O0OO000O0O0OO0 =O00000000O00O0OOO *math .sin (angle )#line:482
    O0OOOO0OO00OOO0OO =O00000000O00O0OOO *math .cos (angle )#line:483
    if direction ==1 :#line:484
        if angle <=1 :#line:485
            angle +=0.15 #line:486
        else :#line:487
            direction =-1 #line:488
    if direction ==-1 :#line:489
        if angle >=-1 :#line:490
            angle -=0.15 #line:491
        else :#line:492
            direction =1 #line:493
    OO0O0000O0O0OO0OO .finalX =O00O0OO000O0O0OO0 #line:494
    OO0O0000O0O0OO0OO .finalY =O0OOOO0OO00OOO0OO #line:495
def refresh (O00000O00O000O0OO ,OO0O00000O0OO0000 ):#line:497
    for O00000OOO0OOOOO00 in range (OO0O00000O0OO0000 ):#line:498
        O00000O00O000O0OO .update ()#line:499
        time .sleep (0.01 )#line:500
def judge (OOO00OO0O00OOOOOO ,O0O000OO00OOOO0O0 ,OO0OOOOOOO0O0O0OO ,OOO0OOO00OO0OO0OO ,O000OOO00O0OOO000 ,O0O0OO0O0OOOOOOO0 ,O00OO0000O0OO00O0 ,O0OOO0O0O0OO00O00 ,OO0OOO0O00O0O0O0O ):#line:502
    global flg ,fff ,f ,border ,borderr #line:503
    if f ==1 :#line:504
        flg =1 #line:505
    for OOO000OOO0OO0OOOO in range (len (OOO00OO0O00OOOOOO .listXY )):#line:506
        if OOO00OO0O00OOOOOO .namelist [OOO000OOO0OO0OOOO ][1 ]==OOO0OOO00OO0OO0OO :#line:507
            border =O00OO0000O0OO00O0 #line:508
        elif OOO00OO0O00OOOOOO .namelist [OOO000OOO0OO0OOOO ][1 ]==O000OOO00O0OOO000 :#line:509
            border =O0OOO0O0O0OO00O00 #line:510
        elif OOO00OO0O00OOOOOO .namelist [OOO000OOO0OO0OOOO ][1 ]==O0O0OO0O0OOOOOOO0 :#line:511
            border =OO0OOO0O00O0O0O0O #line:512
        if O0O000OO00OOOO0O0 >=OOO00OO0O00OOOOOO .listXY [OOO000OOO0OO0OOOO ][0 ]-5 and O0O000OO00OOOO0O0 <=OOO00OO0O00OOOOOO .listXY [OOO000OOO0OO0OOOO ][0 ]+border +5 :#line:513
            if OO0OOOOOOO0O0O0OO >=OOO00OO0O00OOOOOO .listXY [OOO000OOO0OO0OOOO ][1 ]and OO0OOOOOOO0O0O0OO <=OOO00OO0O00OOOOOO .listXY [OOO000OOO0OO0OOOO ][1 ]+border :#line:514
                borderr =border #line:515
                OOO00OO0O00OOOOOO .index =OOO000OOO0OO0OOOO #line:516
                print ("碰到了")#line:517
                flg =1 #line:518
    if OOO00OO0O00OOOOOO .distanceY >300 :#line:519
        fff =1 #line:520
        flg =1 #line:521
def lengths (O000O0OO0O0OOO0O0 ,OOO00000OOO00O000 ):#line:523
    O000O0OO0O0OOO0O0 .distanceY +=OOO00000OOO00O000 #line:524
    O000O0OO0O0OOO0O0 .distanceX +=(OOO00000OOO00O000 *O000O0OO0O0OOO0O0 .finalX )/O000O0OO0O0OOO0O0 .finalY #line:525
def YesOrNo (O00OO0OOOOOO0O000 ):#line:527
    global flg ,fff ,f #line:528
    if flg !=1 and O00OO0OOOOOO0O000 .distanceY >=0 and O00OO0OOOOOO0O000 .distanceY <=300 :#line:529
        lengths (O00OO0OOOOOO0O000 ,2 )#line:530
        O00OO0OOOOOO0O000 .hook .move (290 +O00OO0OOOOOO0O000 .finalX +O00OO0OOOOOO0O000 .distanceX ,58 +O00OO0OOOOOO0O000 .finalY +O00OO0OOOOOO0O000 .distanceY )#line:531
        return 0 ,0 #line:532
    elif flg ==1 and O00OO0OOOOOO0O000 .distanceY >=0 and fff !=1 :#line:533
        f =1 #line:534
        lengths (O00OO0OOOOOO0O000 ,-2 )#line:535
        return 1 ,0 #line:536
    elif flg ==1 and fff ==1 and O00OO0OOOOOO0O000 .distanceY >=0 :#line:537
        f =1 #line:538
        lengths (O00OO0OOOOOO0O000 ,-2 )#line:539
        O00OO0OOOOOO0O000 .hook .move (290 +O00OO0OOOOOO0O000 .finalX +O00OO0OOOOOO0O000 .distanceX ,58 +O00OO0OOOOOO0O000 .finalY +O00OO0OOOOOO0O000 .distanceY )#line:540
        return 0 ,0 #line:541
    else :#line:542
        if fff !=1 :#line:543
            O00OO0OOOOOO0O000 .distanceY =0 #line:544
            flg ,f ,fff ,O00OO0OOOOOO0O000 .isdo =0 ,0 ,0 ,0 #line:545
            return 1 ,1 #line:546
        O00OO0OOOOOO0O000 .distanceY =0 #line:547
        flg ,f ,fff ,O00OO0OOOOOO0O000 .isdo =0 ,0 ,0 ,0 #line:548
        try :#line:549
            O00OO0OOOOOO0O000 .elderGif .stop ()#line:550
            return 0 ,0 #line:551
        except AttributeError :#line:552
            return 0 ,0 #line:553
def playAudio (O0OOO0O0OO00OOO0O ):#line:555
    O00OOO0O0OO0OOO0O =PyQt5_QMediaPlayer ()#line:556
    O00OOO0O0OO0OOO0O .prepare_audio (O0OOO0O0OO00OOO0O )#line:557
    O00OOO0O0OO0OOO0O .play ()#line:558
def change_img (OO0OOO00O00O0OOO0 ,OOO0O0O0OO0000O0O ,OOOO00OO000O00O00 ,O000O0O00O00O00OO ):#line:560
    if OO0OOO00O00O0OOO0 .namelist [OO0OOO00O00O0OOO0 .index ][1 ]==OOO0O0O0OO0000O0O :#line:561
        OO0OOO00O00O0OOO0 .namelist [OO0OOO00O00O0OOO0 .index ][0 ].setBackground ("hook_gold.png")#line:562
    elif OO0OOO00O00O0OOO0 .namelist [OO0OOO00O00O0OOO0 .index ][1 ]==OOOO00OO000O00O00 :#line:563
        OO0OOO00O00O0OOO0 .namelist [OO0OOO00O00O0OOO0 .index ][0 ].setBackground ("hook_diamond.png")#line:564
    else :#line:565
        OO0OOO00O00O0OOO0 .namelist [OO0OOO00O00O0OOO0 .index ][0 ].setBackground ("hook_stone.png")#line:566
def getBorder ():#line:568
    return borderr #line:569
name="VipCode"