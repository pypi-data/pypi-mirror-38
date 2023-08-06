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
    def __init__ (OOO0OO0OO0O00O00O ):#line:30
        super ().__init__ ()#line:31
        OOO0OO0OO0O00O00O .setObjectName ("dialog")#line:32
        global parwidth #line:33
        parwidth =OOO0OO0OO0O00O00O .width ()+200 #line:34
    def setBackgroundColor (O0O000OO00OOO0OOO ,O0000O00O0O0OOOOO ):#line:35
        O0O000OO00OOO0OOO .setStyleSheet ("#dialog{background-color:"+O0000O00O0O0OOOOO +"}")#line:36
    def setBackground (O0OOO00OO0OO00O0O ,O0000O0O0OO000O00 ):#line:37
        O0OOO00OO0OO00O0O .setStyleSheet ("#dialog{border-image:url(RESOURCE/drawable/"+O0000O0O0OO000O00 +")}")#line:38
    def setResize (O0O0000000000O00O ,O00O00OO0O0O00O00 ,O00O00O0O0OO0O0O0 ):#line:40
        O0O0000000000O00O .resize (O00O00OO0O0O00O00 ,O00O00O0O0OO0O0O0 )#line:41
    def addBodyButton (O000000OO000O0000 ,O00O0000O0OO00OOO ):#line:43
        O000000OO000O0000 .bodylabel =O00O0000O0OO00OOO #line:44
        O000000OO000O0000 .head =PyQt5_QPushButton (O000000OO000O0000 ,400 ,300 ,160 ,130 )#line:45
        O000000OO000O0000 .head .setBackgroundColor ("rgba(100,0, 200, 0)")#line:46
        O000000OO000O0000 .body =PyQt5_QPushButton (O000000OO000O0000 ,445 ,430 ,70 ,80 )#line:48
        O000000OO000O0000 .body .setBackgroundColor ("rgba(100,0, 200, 0)")#line:49
        O000000OO000O0000 .leftArm =PyQt5_QPushButton (O000000OO000O0000 ,420 ,430 ,40 ,30 )#line:51
        O000000OO000O0000 .leftArm .setBackgroundColor ("rgba(0,0, 0, 0)")#line:52
        O000000OO000O0000 .rightArm =PyQt5_QPushButton (O000000OO000O0000 ,505 ,430 ,50 ,30 )#line:54
        O000000OO000O0000 .rightArm .setBackgroundColor ("rgba(0,0, 0, 0)")#line:55
        O000000OO000O0000 .leftFoot =PyQt5_QPushButton (O000000OO000O0000 ,440 ,500 ,30 ,30 )#line:57
        O000000OO000O0000 .leftFoot .setBackgroundColor ("rgba(0,0, 0, 0)")#line:58
        O000000OO000O0000 .rightFoot =PyQt5_QPushButton (O000000OO000O0000 ,500 ,500 ,30 ,30 )#line:60
        O000000OO000O0000 .rightFoot .setBackgroundColor ("rgba(0,0, 0, 0)")#line:61
        O000000OO000O0000 .head .clicked .connect (O000000OO000O0000 .headClicked )#line:63
        O000000OO000O0000 .leftArm .clicked .connect (O000000OO000O0000 .armClicked )#line:64
        O000000OO000O0000 .rightArm .clicked .connect (O000000OO000O0000 .armClicked )#line:65
        O000000OO000O0000 .rightFoot .clicked .connect (O000000OO000O0000 .rightFootClicked )#line:66
        O000000OO000O0000 .leftFoot .clicked .connect (O000000OO000O0000 .leftFootClicked )#line:67
        O000000OO000O0000 .body .clicked .connect (O000000OO000O0000 .bodyClicked )#line:68
    def armClicked (OOOOO0OOOOOOO0O00 ):#line:69
        OOOOO0OOOOOOO0O00 .neibu2 ('main_arm')#line:70
        OOOOO0OOOOOOO0O00 .neibu1 ('main_arm')#line:75
    def leftFootClicked (O0O000OO0O0O00OO0 ):#line:76
        O0O000OO0O0O00OO0 .neibu2 ('main_leftFoot')#line:77
        O0O000OO0O0O00OO0 .neibu1 ('main_leftFoot')#line:78
    def rightFootClicked (OO00O0000OOO0O0O0 ):#line:79
        OO00O0000OOO0O0O0 .neibu2 ('main_rightFoot')#line:80
        OO00O0000OOO0O0O0 .neibu1 ('main_rightFoot')#line:81
    def bodyClicked (OOO00OO00000OO00O ):#line:82
        OOO00OO00000OO00O .neibu2 ('main_body')#line:83
        OOO00OO00000OO00O .neibu1 ('main_body')#line:84
    def headClicked (OOOOOO000O00O0000 ):#line:85
        OOOOOO000O00O0000 .neibu2 ('main_head')#line:86
        OOOOOO000O00O0000 .neibu1 ('main_head')#line:87
    def neibu2 (OO00OO0OO0OO0O0OO ,O0O0000OO00O0OOO0 ):#line:89
        OO00OO0OO0OO0O0OO .neigif =PyQt5_QMovie (O0O0000OO00O0OOO0 +'.gif')#line:91
        OO00OO0OO0OO0O0OO .neigif .setScaledSize (OO00OO0OO0OO0O0OO .bodylabel .size ())#line:93
        OO00OO0OO0OO0O0OO .bodylabel .setMovie (OO00OO0OO0OO0O0OO .neigif )#line:95
        OO00OO0OO0OO0O0OO .neigif .start ()#line:97
        OO00OO0OO0OO0O0OO .frameCount =OO00OO0OO0OO0O0OO .neigif .frameCount ()#line:98
        OO00OO0OO0OO0O0OO .neigif .frameChanged .connect (OO00OO0OO0OO0O0OO .neibu3 )#line:100
    def neibu3 (OOOO0O000O000OO0O ):#line:101
        OOOO0O000O000OO0O .frameCount -=1 #line:103
        if OOOO0O000O000OO0O .frameCount ==0 :#line:105
            OOOO0O000O000OO0O .neigif .stop ()#line:107
            OOOO0O000O000OO0O .neigif =PyQt5_QMovie ('main_lion.gif')#line:109
            OOOO0O000O000OO0O .neigif .setScaledSize (OOOO0O000O000OO0O .bodylabel .size ())#line:110
            OOOO0O000O000OO0O .bodylabel .setMovie (OOOO0O000O000OO0O .neigif )#line:112
            OOOO0O000O000OO0O .neigif .start ()#line:114
    def neibu1 (OOOO00OO0O0O0O00O ,O0O0O000O0OO0O000 ):#line:116
        OO00OOO00OOO0O000 =PyQt5_QMediaPlayer ()#line:118
        OO00OOO00OOO0O000 .prepare_audio (O0O0O000O0OO0O000 +'.wav')#line:120
        OO00OOO00OOO0O000 .play ()#line:122
class PyQt5_QPushButton (QPushButton ):#line:125
    def __init__ (O0OOOO00OO000O00O ,O00O00O0000OO0O0O ,x =0 ,y =0 ,width =113 ,height =32 ):#line:126
        super ().__init__ (O00O00O0000OO0O0O )#line:127
        O0OOOO00OO000O00O .setGeometry (x ,y ,width ,height )#line:128
    def setBackground (O0O00OO00O0O00OO0 ,OOO0O00000OOOOO00 ):#line:130
        O0O00OO00O0O00OO0 .setStyleSheet (O0O00OO00O0O00OO0 .styleSheet ()+"QPushButton{border-image:url(RESOURCE/drawable/"+OOO0O00000OOOOO00 +")}")#line:132
    def setPressedBackground (O00OOOOOOO0O00OOO ,O0O0000OO0O00O000 ):#line:134
        O00OOOOOOO0O00OOO .setStyleSheet (O00OOOOOOO0O00OOO .styleSheet ()+"QPushButton:pressed{border-image:url(RESOURCE/drawable/"+O0O0000OO0O00O000 +")}")#line:136
    def setBackgroundColor (O0OOO00O00O0OO0O0 ,O00O00OO0OOOOO0OO ):#line:138
        O0OOO00O00O0OO0O0 .setStyleSheet (O0OOO00O00O0OO0O0 .styleSheet ()+"QPushButton{background-color:"+O00O00OO0OOOOO0OO +"}")#line:139
    def setTextColor (OO0OO0OO00O0OOOOO ,O00OOOO0OOO0O0O0O ):#line:141
        OO0OO0OO00O0OOOOO .setStyleSheet (OO0OO0OO00O0OOOOO .styleSheet ()+"QPushButton{color:"+O00OOOO0OOO0O0O0O +"}")#line:142
    def setPressedTextColor (OO0O00OO0O0OO0O0O ,OOOO00O00OOO00O00 ):#line:144
        OO0O00OO0O0OO0O0O .setStyleSheet (OO0O00OO0O0OO0O0O .styleSheet ()+"QPushButton:pressed{color:"+OOOO00O00OOO00O00 +"}")#line:145
    def setFontSize (O00O00000OO000OOO ,O0000000O0O0OOOOO ):#line:147
        O000000OOOOO00O00 =QFont ()#line:148
        O000000OOOOO00O00 .setPixelSize (O0000000O0O0OOOOO )#line:149
        O00O00000OO000OOO .setFont (O000000OOOOO00O00 )#line:150
class PyQt5_QLineEdit (QLineEdit ):#line:153
    Password =QLineEdit .Password #line:154
    Normal =QLineEdit .Normal #line:155
    NoEcho =QLineEdit .NoEcho #line:156
    PasswordEchoOnEdit =QLineEdit .PasswordEchoOnEdit #line:157
    def __init__ (OOOO00OOO0OOOOOO0 ,O00O0OOO00O0OO0O0 ,x =0 ,y =0 ,width =113 ,height =21 ):#line:159
        super ().__init__ (O00O0OOO00O0OO0O0 )#line:160
        OOOO00OOO0OOOOOO0 .setGeometry (x ,y ,width ,height )#line:161
        OOOO00OOO0OOOOOO0 .setFontSize (14 )#line:162
        OOOO00OOO0OOOOOO0 .setAlignment (Qt .AlignVCenter )#line:163
    def setFontSize (O00O0OO00O0OOO00O ,O0O00OOOOOOO00O0O ):#line:165
        O0OOO00OOOOOOOO0O =QFont ()#line:166
        O0OOO00OOOOOOOO0O .setPixelSize (O0O00OOOOOOO00O0O )#line:167
        O00O0OO00O0OOO00O .setFont (O0OOO00OOOOOOOO0O )#line:168
    def setBackground (OOO0OOOO0O0OO00OO ,O00000OO0OO000OO0 ):#line:170
        OOO0OOOO0O0OO00OO .setStyleSheet (OOO0OOOO0O0OO00OO .styleSheet ()+"border-image:url(RESOURCE/drawable/"+O00000OO0OO000OO0 +");")#line:171
    def setBackgroundColor (OOO0O00O00OO000O0 ,O0OOO0O00O0OOOOO0 ):#line:173
        OOO0O00O00OO000O0 .setStyleSheet (OOO0O00O00OO000O0 .styleSheet ()+"background-color:"+O0OOO0O00O0OOOOO0 +";")#line:174
    def setTextColor (OO00OO0000O0000O0 ,OO0O000OOO0OOOOO0 ):#line:176
        OO00OO0000O0000O0 .setStyleSheet (OO00OO0000O0000O0 .styleSheet ()+"color:"+OO0O000OOO0OOOOO0 +";")#line:177
    def setDisplayMode (O00OOOO0000OOOOO0 ,O0O0OO0OO000000OO ):#line:179
        if O0O0OO0OO000000OO ==PyQt5_QLineEdit .Password :#line:180
            O00OOOO0000OOOOO0 .setEchoMode (O0O0OO0OO000000OO )#line:181
        elif O0O0OO0OO000000OO ==PyQt5_QLineEdit .Normal :#line:182
            O00OOOO0000OOOOO0 .setEchoMode (O0O0OO0OO000000OO )#line:183
        elif O0O0OO0OO000000OO ==PyQt5_QLineEdit .NoEcho :#line:184
            O00OOOO0000OOOOO0 .setEchoMode (O0O0OO0OO000000OO )#line:185
        elif O0O0OO0OO000000OO ==PyQt5_QLineEdit .PasswordEchoOnEdit :#line:186
            O00OOOO0000OOOOO0 .setEchoMode (O0O0OO0OO000000OO )#line:187
class PyQt5_Qlabel (QLabel ):#line:190
    clicked =pyqtSignal (QMouseEvent )#line:191
    def __init__ (O0O0OO00000OOOO00 ,O0OOOOOO00O0OO0O0 ,x =0 ,y =0 ,width =60 ,height =16 ):#line:192
        super ().__init__ (O0OOOOOO00O0OO0O0 )#line:193
        O0O0OO00000OOOO00 .widget =O0OOOOOO00O0OO0O0 #line:194
        O0O0OO00000OOOO00 .zeze =True #line:195
        O0O0OO00000OOOO00 .setGeometry (x ,y ,width ,height )#line:196
    def setFontSize (OO0OOOOO000OO00O0 ,O000OOO0OOO0OO00O ):#line:197
        OO0OO0OO000000OOO =QFont ()#line:198
        OO0OO0OO000000OOO .setPixelSize (O000OOO0OOO0OO00O )#line:199
        OO0OOOOO000OO00O0 .setFont (OO0OO0OO000000OOO )#line:200
    def setFontFitSize (OO0O00000OOOOOOO0 ,OO0O0O0OO0O0O000O ):#line:201
        O0OOOO0O0OOO0O0O0 =QFont ()#line:202
        O0OOOO0O0OOO0O0O0 .setPointSize (OO0O0O0OO0O0O000O )#line:203
        OO0O00000OOOOOOO0 .setFont (O0OOOO0O0OOO0O0O0 )#line:204
    def setBackground (OO0O000OOO0OO0OOO ,OO0OO00000OOOOO0O ):#line:205
        OO0O000OOO0OO0OOO .setStyleSheet (OO0O000OOO0OO0OOO .styleSheet ()+"border-image:url(RESOURCE/drawable/"+OO0OO00000OOOOO0O +");")#line:206
    def setBackgroundColor (O00OOOO0OOOO0000O ,O00000O00OO0O0O0O ):#line:208
        O00OOOO0OOOO0000O .setStyleSheet (O00OOOO0OOOO0000O .styleSheet ()+"background-color:"+O00000O00OO0O0O0O +";")#line:209
    def setTextColor (O0O00000O0O00OO00 ,OO000OOO0OOO0O0OO ):#line:211
        O0O00000O0O00OO00 .setStyleSheet (O0O00000O0O00OO00 .styleSheet ()+"color:"+OO000OOO0OOO0O0OO +";")#line:212
    def mouseReleaseEvent (OOOO0O0OOOO0O0000 ,OOO0O0O000O00O0OO ):#line:213
        OOOO0O0OOOO0O0000 .released .emit (OOO0O0O000O00O0OO )#line:214
    released =pyqtSignal (QMouseEvent )#line:215
    pressed =pyqtSignal (QEvent )#line:216
    def mousePressEvent (O00O0OOO0000O0OO0 ,OO000O000O0O00O00 ):#line:217
        O00O0OOO0000O0OO0 .pressed .emit (OO000O000O0O00O00 )#line:218
        if OO000O000O0O00O00 .buttons ()==Qt .LeftButton :#line:219
            O00O0OOO0000O0OO0 .clicked .emit (OO000O000O0O00O00 )#line:220
    moved =pyqtSignal (QMouseEvent )#line:221
    def mouseMoveEvent (O0O0O000OOO0O0O00 ,OOOO00O00OO00OO0O ):#line:222
        O0O0O000OOO0O0O00 .moved .emit (OOOO00O00OO00OO0O )#line:223
    doubleclicked =pyqtSignal (QMouseEvent )#line:224
    def mouseDoubleClickEvent (O000OOOOO00O00000 ,OOO00OO0O0O000O00 ):#line:225
        if OOO00OO0O0O000O00 .buttons ()==Qt .LeftButton :#line:226
            O000OOOOO00O00000 .doubleclicked .emit (OOO00OO0O0O000O00 )#line:227
    entered =pyqtSignal (QEnterEvent )#line:228
    def enterEvent (O0OOO0OOOO00O0O00 ,OO0O0OO00O00000OO ):#line:229
        O0OOO0OOOO00O0O00 .entered .emit (OO0O0OO00O00000OO )#line:230
    leaved =pyqtSignal (QEvent )#line:232
    def leaveEvent (OOO00OOO00OOO0000 ,O0000OO00OO0O0OOO ):#line:233
        OOO00OOO00OOO0000 .leaved .emit (O0000OO00OO0O0OOO )#line:234
    def setSize (OO0O00O00O00O0OOO ,O0OOOOO00O0OOOOOO ):#line:237
        OO0O00O00O00O0OOO .setFixedSize (O0OOOOO00O0OOOOOO )#line:238
    def refresh (O0O0O00OO00OOO0OO ):#line:239
        if O0O0O00OO00OOO0OO .zeze :#line:240
            O0O0O00OO00OOO0OO .widget .resize (O0O0O00OO00OOO0OO .widget .width ()+1 ,O0O0O00OO00OOO0OO .widget .height ()+1 )#line:241
            O0O0O00OO00OOO0OO .zeze =False #line:242
        else :#line:243
            O0O0O00OO00OOO0OO .widget .resize (O0O0O00OO00OOO0OO .widget .width ()-1 ,O0O0O00OO00OOO0OO .widget .height ()-1 )#line:244
            O0O0O00OO00OOO0OO .zeze =True #line:245
class PyQt5_QMovie (QMovie ):#line:247
    def __init__ (OO0000O0O0OO000O0 ,OO00OOO000OOOO000 ):#line:248
        super ().__init__ ("RESOURCE/gif/"+OO00OOO000OOOO000 )#line:249
class PyQt5_QMediaPlayer ():#line:251
    def __init__ (OOOO0000O0OOOO0O0 ):#line:252
        pygame .mixer .init ()#line:253
        OOOO0000O0OOOO0O0 .music =pygame .mixer .music #line:254
    def prepare_audio (OO0OOO0OO00O00O0O ,OO0O0000O000OO0OO ):#line:255
        OO0OOO0OO00O00O0O .music .load ("RESOURCE/audio/"+OO0O0000O000OO0OO )#line:256
    def prepare_voice (OOO000O0OOO0OO000 ,O000O0O0O0O0O00O0 ):#line:257
        OOO000O0OOO0OO000 .music .load ("RESOURCE/voice/"+O000O0O0O0O0O00O0 )#line:258
    def play (OOO00O00O00O0O0O0 ,loops =1 ,start =0.0 ):#line:259
        if loops ==0 :#line:260
            OOO00O00O00O0O0O0 .music .play (-1 ,start )#line:261
        elif loops <0 :#line:262
            pass #line:263
        elif loops >0 :#line:264
            OOO00O00O00O0O0O0 .music .play (loops -1 ,start )#line:265
    def stop (O000O00OO0OO0000O ):#line:266
        O000O00OO0OO0000O .music .stop ()#line:267
    def pause (OOO0O0O00OO000000 ):#line:268
        OOO0O0O00OO000000 .music .pause ()#line:269
    def setVolume (OO0O0O0O000OOOOOO ,OOO0OO0O0O00O0O00 ):#line:270
        OO0O0O0O000OOOOOO .music .set_volume (OOO0OO0O0O00O0O00 )#line:271
    def isPlaying (O0OOOO00O0OO00OO0 ):#line:272
        if O0OOOO00O0OO00OO0 .music .get_busy ()==1 :#line:273
            return True #line:274
        else :#line:275
            return False #line:276
class PyQt5_QCheckBox (QCheckBox ):#line:280
    def __init__ (O0OO0O00O00O0OO00 ,OOOOOOOO0OO00O00O ,x =0 ,y =0 ,width =20 ,height =20 ):#line:281
        super ().__init__ (OOOOOOOO0OO00O00O )#line:282
        O0OO0O00O00O0OO00 .setGeometry (x ,y ,width ,height )#line:283
        O0OO0O00O00O0OO00 .isIndicator =True #line:284
        O0OO0O00O00O0OO00 .image_name_normal =""#line:285
        O0OO0O00O00O0OO00 .image_name_pressed =""#line:286
    def setIndicator (O0O0000O0OOO0O0OO ,OOOOO0OO0000OO0OO ):#line:288
        O0O0000O0OOO0O0OO .isIndicator =OOOOO0OO0000OO0OO #line:289
        O0O0000O0OOO0O0OO .setStyleSheet ("")#line:290
        if O0O0000O0OOO0O0OO .image_name_normal !="":#line:291
            O0O0000O0OOO0O0OO .setUncheckedBackground (O0O0000O0OOO0O0OO .image_name_normal )#line:292
        if O0O0000O0OOO0O0OO .image_name_pressed !="":#line:293
            O0O0000O0OOO0O0OO .setCheckedBackground (O0O0000O0OOO0O0OO .image_name_pressed )#line:294
    def setUncheckedBackground (OO0O0OOOOOO000000 ,OO0O0OO000O0OO00O ):#line:296
        if OO0O0OOOOOO000000 .isIndicator :#line:297
            OO0O0OOOOOO000000 .setStyleSheet (OO0O0OOOOOO000000 .styleSheet ()+"QCheckBox:unchecked{width:"+str (OO0O0OOOOOO000000 .width ())+"px;height:"+str (OO0O0OOOOOO000000 .height ())+"px;border-image:url(RESOURCE/drawable/"+OO0O0OO000O0OO00O +")}")#line:300
        else :#line:301
            OO0O0OOOOOO000000 .setStyleSheet (OO0O0OOOOOO000000 .styleSheet ()+"QCheckBox:indicator:unchecked{width:"+str (OO0O0OOOOOO000000 .width ())+"px;height:"+str (OO0O0OOOOOO000000 .height ())+"px;border-image:url(RESOURCE/drawable/"+OO0O0OO000O0OO00O +")}")#line:304
        OO0O0OOOOOO000000 .image_name_normal =OO0O0OO000O0OO00O #line:305
    def setCheckedBackground (OO00O000O0OOOOOOO ,O0OOOOO00OOO00000 ):#line:307
        if OO00O000O0OOOOOOO .isIndicator :#line:308
            OO00O000O0OOOOOOO .setStyleSheet (OO00O000O0OOOOOOO .styleSheet ()+"QCheckBox:checked{width:"+str (OO00O000O0OOOOOOO .width ())+"px;height:"+str (OO00O000O0OOOOOOO .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OOOOO00OOO00000 +")}")#line:311
        else :#line:312
            OO00O000O0OOOOOOO .setStyleSheet (OO00O000O0OOOOOOO .styleSheet ()+"QCheckBox:indicator:checked{width:"+str (OO00O000O0OOOOOOO .width ())+"px;height:"+str (OO00O000O0OOOOOOO .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OOOOO00OOO00000 +")}")#line:315
        OO00O000O0OOOOOOO .image_name_pressed =O0OOOOO00OOO00000 #line:316
class PyQt5_QRadioButton (QRadioButton ):#line:319
    def __init__ (O000OO0O0OO0OOO00 ,OOOO0OOO00000O0OO ,x =0 ,y =0 ,width =20 ,height =20 ):#line:320
        super ().__init__ (OOOO0OOO00000O0OO )#line:321
        O000OO0O0OO0OOO00 .setGeometry (x ,y ,width ,height )#line:322
        O000OO0O0OO0OOO00 .isIndicator =True #line:323
        O000OO0O0OO0OOO00 .image_name_normal =""#line:324
        O000OO0O0OO0OOO00 .image_name_pressed =""#line:325
    def setFontSize (O0O0O0000O00OO000 ,O0OO0O000O000O0OO ):#line:327
        O00O0O000000OOOOO =QFont ()#line:328
        O00O0O000000OOOOO .setPixelSize (O0OO0O000O000O0OO )#line:329
        O0O0O0000O00OO000 .setFont (O00O0O000000OOOOO )#line:330
    def setTextColor (O0OOOOO0O000OOO00 ,O0O00O000O00000O0 ):#line:332
        O0OOOOO0O000OOO00 .setStyleSheet (O0OOOOO0O000OOO00 .styleSheet ()+"color:"+O0O00O000O00000O0 +";")#line:333
    def setIndicator (O0OOO0OO000O0000O ,O0O0O0OO0OOO0000O ):#line:335
        O0OOO0OO000O0000O .isIndicator =O0O0O0OO0OOO0000O #line:336
        O0OOO0OO000O0000O .setStyleSheet ("")#line:337
        if O0OOO0OO000O0000O .image_name_normal !="":#line:338
            O0OOO0OO000O0000O .setUncheckedBackground (O0OOO0OO000O0000O .image_name_normal )#line:339
        if O0OOO0OO000O0000O .image_name_pressed !="":#line:340
            O0OOO0OO000O0000O .setCheckedBackground (O0OOO0OO000O0000O .image_name_pressed )#line:341
    def setUncheckedBackground (OO0O0OO000O00O00O ,O0O0O0OO000O0OO0O ):#line:343
        if OO0O0OO000O00O00O .isIndicator :#line:344
            OO0O0OO000O00O00O .setStyleSheet (OO0O0OO000O00O00O .styleSheet ()+"QRadioButton:unchecked{width:"+str (OO0O0OO000O00O00O .width ())+"px;height:"+str (OO0O0OO000O00O00O .height ())+"px;border-image:url(RESOURCE/drawable/"+O0O0O0OO000O0OO0O +")}")#line:347
        else :#line:348
            OO0O0OO000O00O00O .setStyleSheet (OO0O0OO000O00O00O .styleSheet ()+"QRadioButton:indicator:unchecked{width:"+str (OO0O0OO000O00O00O .width ())+"px;height:"+str (OO0O0OO000O00O00O .height ())+"px;border-image:url(RESOURCE/drawable/"+O0O0O0OO000O0OO0O +")}")#line:351
        OO0O0OO000O00O00O .image_name_normal =O0O0O0OO000O0OO0O #line:352
    def setCheckedBackground (O0000OO0OOO000O00 ,OOOOOO0O0OOOOOOO0 ):#line:354
        if O0000OO0OOO000O00 .isIndicator :#line:355
            O0000OO0OOO000O00 .setStyleSheet (O0000OO0OOO000O00 .styleSheet ()+"QRadioButton:checked{width:"+str (O0000OO0OOO000O00 .width ())+"px;height:"+str (O0000OO0OOO000O00 .height ())+"px;border-image:url(RESOURCE/drawable/"+OOOOOO0O0OOOOOOO0 +")}")#line:358
        else :#line:359
            O0000OO0OOO000O00 .setStyleSheet (O0000OO0OOO000O00 .styleSheet ()+"QRadioButton:indicator:checked{width:"+str (O0000OO0OOO000O00 .width ())+"px;height:"+str (O0000OO0OOO000O00 .height ())+"px;border-image:url(RESOURCE/drawable/"+OOOOOO0O0OOOOOOO0 +")}")#line:362
        O0000OO0OOO000O00 .image_name_pressed =OOOOOO0O0OOOOOOO0 #line:363
class PyQt5_QGroupBox (QGroupBox ):#line:366
    def __init__ (O0000000OO0O00OOO ,OOOO000OOO0OO000O ,x =0 ,y =0 ,width =120 ,height =80 ):#line:367
        super ().__init__ (OOOO000OOO0OO000O )#line:368
        O0000000OO0O00OOO .setGeometry (x ,y ,width ,height )#line:369
        O0000000OO0O00OOO .setObjectName ("groupbox")#line:370
    def setBackground (O0O0O00000O0OOOOO ,O0000OO0OO0O0OOO0 ):#line:372
        O0O0O00000O0OOOOO .setStyleSheet ("#groupbox{border-image:url(RESOURCE/drawable/"+O0000OO0OO0O0OOO0 +")}")#line:373
    def setBackgroundColor (O0000OO00O0OOOOOO ,O000OO0O0O0OO00OO ):#line:375
        O0000OO00O0OOOOOO .setStyleSheet ("#groupbox{background-color:"+O000OO0O0O0OO00OO +"}")#line:376
    def setBorderWidth (OOO00OOO0OOO0O000 ,OO000000OOOO000OO ):#line:378
        OOO00OOO0OOO0O000 .setStyleSheet (OOO00OOO0OOO0O000 .styleSheet ()+"border-width:"+str (OO000000OOOO000OO )+"px;border-style:solid;")#line:379
def getQuestion (OO0OO0000OOO00OO0 ):#line:382
    try :#line:383
        O0O0000O0000O0OO0 =ipStr +'ti/findById.do?id=%d'%OO0OO0000OOO00OO0 #line:385
        O0O0000O0000O0OO0 =urllib .request .Request (url =O0O0000O0000O0OO0 )#line:386
        O0O0000O0000O0OO0 .add_header ('Content-Type','application/json')#line:387
        OO00O0OO0OO00OOO0 =urllib .request .urlopen (O0O0000O0000O0OO0 )#line:388
    except urllib .error .URLError as O00000OO00O00OO00 :#line:389
        OO00OO000OOOO00OO ={"id":1 ,"wenti":"由于网络问题未找到所需内容，请检查您的网络","daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:390
        return OO00OO000OOOO00OO #line:391
    OO00OO000OOOO00OO =json .loads (OO00O0OO0OO00OOO0 .read ().decode ('utf-8'))#line:393
    if OO00OO000OOOO00OO :#line:395
        if OO00OO000OOOO00OO ["state"]!=0 :#line:396
            return {"id":1 ,"wenti":OO00OO000OOOO00OO ["message"],"daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:397
        else :#line:398
            return OO00OO000OOOO00OO ["data"]#line:399
def reductionRadioBtn (O000O0OO00OO0OO00 ):#line:400
    for O000O0OOO0OO0O0OO in range (len (O000O0OO00OO0OO00 )):#line:401
        O000O0OO00OO0OO00 [O000O0OOO0OO0O0OO ].setCheckable (False )#line:402
        O000O0OO00OO0OO00 [O000O0OOO0OO0O0OO ].setCheckable (True )#line:403
class PyQt5_QSystemTrayIcon (QSystemTrayIcon ):#line:404
    def __init__ (OOOO00000OOOOO0O0 ,parent =None ):#line:405
        super (PyQt5_QSystemTrayIcon ,OOOO00000OOOOO0O0 ).__init__ (parent )#line:406
        OOOO00000OOOOO0O0 .menu =QMenu ()#line:407
        OOOO00000OOOOO0O0 .setContextMenu (OOOO00000OOOOO0O0 .menu )#line:408
    def addMenu (O00O000000O0O0O00 ,OOOOOO0000O0O0O00 ):#line:409
        O00O000000O0O0O00 .menuAction =QAction (OOOOOO0000O0O0O00 ,O00O000000O0O0O00 )#line:410
        O00O000000O0O0O00 .menu .addAction (O00O000000O0O0O00 .menuAction )#line:411
        return O00O000000O0O0O00 .menuAction #line:412
    def _setIcon (O0OO0OOO0OO00OO0O ,O000O0OO00O0OO00O ):#line:413
        O0OO0OOO0OO00OO0O .setIcon (QIcon ("RESOURCE/drawable/"+O000O0OO00O0OO00O ))#line:414
class PyQt5_Animation (QPropertyAnimation ):#line:417
    animFinished =pyqtSignal ()#line:418
    def __init__ (OO0000000OO0OO00O ,QWidget =None ):#line:419
        super (PyQt5_Animation ,OO0000000OO0OO00O ).__init__ ()#line:420
        OO0000000OO0OO00O .setPropertyName (b"geometry")#line:421
        OO0000000OO0OO00O .setTargetObject (QWidget )#line:422
        OO0000000OO0OO00O .finished .connect (OO0000000OO0OO00O .aFinished )#line:423
        OO0000000OO0OO00O .widget =QWidget #line:424
        OO0000000OO0OO00O .valueChanged .connect (OO0000000OO0OO00O .up )#line:425
        OO0000000OO0OO00O .ze =True #line:426
    def up (OOO0O0O0O00O00OO0 ):#line:427
        if OOO0O0O0O00O00OO0 .ze :#line:428
            OOO0O0O0O00O00OO0 .widget .resize (OOO0O0O0O00O00OO0 .widget .width ()+1 ,OOO0O0O0O00O00OO0 .widget .height ()+1 )#line:429
            OOO0O0O0O00O00OO0 .ze =False #line:430
        else :#line:431
            OOO0O0O0O00O00OO0 .widget .resize (OOO0O0O0O00O00OO0 .widget .width ()-1 ,OOO0O0O0O00O00OO0 .widget .height ()-1 )#line:432
            OOO0O0O0O00O00OO0 .ze =True #line:433
    def setStartValues (OO0000OO00OO0OOO0 ,OO00O00O0OO0O000O ,OOOOOOOOOOO0O0000 ,O000000OO0O00OOO0 ,O0000OO000O0OO0O0 ):#line:435
        OO0000OO00OO0OOO0 .setStartValue (QRect (OO00O00O0OO0O000O ,OOOOOOOOOOO0O0000 ,O000000OO0O00OOO0 ,O0000OO000O0OO0O0 ))#line:436
    def setEndValues (OOO00000O0OOOOOOO ,O00OOO000OO0O000O ,O00O0OO000O000OO0 ,O00O0OO0O00O0OO0O ,O000OO0O0OO00O000 ):#line:437
        OOO00000O0OOOOOOO .setEndValue (QRect (O00OOO000OO0O000O ,O00O0OO000O000OO0 ,O00O0OO0O00O0OO0O ,O000OO0O0OO00O000 ))#line:438
    def setMode (O0O0OO00000000O0O ,O0OO0OOO000O0O00O ):#line:439
        O0O0OO00000000O0O .setEasingCurve (O0OO0OOO000O0O00O )#line:440
    def aFinished (OO00000OOOOOO0O0O ):#line:441
        OO00000OOOOOO0O0O .animFinished .emit ()#line:442
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
    def __init__ (O0O0OO00OO0000000 ):#line:459
        super ().__init__ ()#line:460
        O0O0OO00OO0000000 .resize (340 ,340 )#line:461
        O0O0OO00OO0000000 .setObjectName ("FramelessBox")#line:462
        O0O0OO00OO0000000 .setWindowFlags (O0O0OO00OO0000000 .windowFlags ()|Qt .FramelessWindowHint )#line:463
    def setWindowsTop (OO0O0O0O0O0000OOO ,O0O00O0O0000OOOOO ):#line:465
        if O0O00O0O0000OOOOO :#line:466
            OO0O0O0O0O0000OOO .setWindowFlags (OO0O0O0O0O0000OOO .windowFlags ()|Qt .WindowStaysOnTopHint )#line:467
    def setResize (OOOO0O0O00O00OOOO ,OO0OOO0000000OOOO ,O0O00OOOOO000O00O ):#line:468
        OOOO0O0O00O00OOOO .resize (OO0OOO0000000OOOO ,O0O00OOOOO000O00O )#line:469
    def setWindowsTransparent (OO000O00000O0O0OO ,OO000000OO0OOO0OO ):#line:470
        if OO000000OO0OOO0OO :#line:471
            OO000O00000O0O0OO .setAttribute (Qt .WA_TranslucentBackground ,True )#line:472
def getDesktopWidth ():#line:474
    return QApplication .desktop ().width ()#line:475
def getDesktopHeight ():#line:477
    return QApplication .desktop ().height ()#line:478
def rock (O0OOO0O0000O000O0 ,O0000OOO00OOO0OOO ):#line:480
    global angle ,direction #line:481
    O0O00O00OO0O000OO =O0000OOO00OOO0OOO *math .sin (angle )#line:482
    OO00OOOOO0O00O0OO =O0000OOO00OOO0OOO *math .cos (angle )#line:483
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
    O0OOO0O0000O000O0 .finalX =O0O00O00OO0O000OO #line:494
    O0OOO0O0000O000O0 .finalY =OO00OOOOO0O00O0OO #line:495
def refresh (O000O0O0OOOOOOO00 ,O00OO0000O0O0OOOO ):#line:497
    for O00O0O000OO0OO000 in range (O00OO0000O0O0OOOO ):#line:498
        O000O0O0OOOOOOO00 .update ()#line:499
        time .sleep (0.01 )#line:500
def judge (OO000OOO0000OOOO0 ,OO00OOO000OO00OOO ,O0O0O00OO00OO00O0 ,O0OOO0O0000000OO0 ,OOOOOO0O00OOOOO0O ,OO00O0OO00O0OOO0O ,O0000000O0O000O0O ,OO00O0O0O0O0O0OO0 ,O00000OOOOOOOO000 ):#line:502
    global flg ,fff ,f ,border ,borderr #line:503
    if f ==1 :#line:504
        flg =1 #line:505
    for O0OOOOO0OOO000OOO in range (len (OO000OOO0000OOOO0 .listXY )):#line:506
        if OO000OOO0000OOOO0 .namelist [O0OOOOO0OOO000OOO ][1 ]==O0OOO0O0000000OO0 :#line:507
            border =O0000000O0O000O0O #line:508
        elif OO000OOO0000OOOO0 .namelist [O0OOOOO0OOO000OOO ][1 ]==OOOOOO0O00OOOOO0O :#line:509
            border =OO00O0O0O0O0O0OO0 #line:510
        elif OO000OOO0000OOOO0 .namelist [O0OOOOO0OOO000OOO ][1 ]==OO00O0OO00O0OOO0O :#line:511
            border =O00000OOOOOOOO000 #line:512
        if OO00OOO000OO00OOO >=OO000OOO0000OOOO0 .listXY [O0OOOOO0OOO000OOO ][0 ]-5 and OO00OOO000OO00OOO <=OO000OOO0000OOOO0 .listXY [O0OOOOO0OOO000OOO ][0 ]+border +5 :#line:513
            if O0O0O00OO00OO00O0 >=OO000OOO0000OOOO0 .listXY [O0OOOOO0OOO000OOO ][1 ]and O0O0O00OO00OO00O0 <=OO000OOO0000OOOO0 .listXY [O0OOOOO0OOO000OOO ][1 ]+border :#line:514
                borderr =border #line:515
                OO000OOO0000OOOO0 .index =O0OOOOO0OOO000OOO #line:516
                print ("碰到了")#line:517
                flg =1 #line:518
    if OO000OOO0000OOOO0 .distanceY >300 :#line:519
        fff =1 #line:520
        flg =1 #line:521
def lengths (O00OO0OO0OO00OOO0 ,OOO000OO0O0OO00OO ):#line:523
    O00OO0OO0OO00OOO0 .distanceY +=OOO000OO0O0OO00OO #line:524
    O00OO0OO0OO00OOO0 .distanceX +=(OOO000OO0O0OO00OO *O00OO0OO0OO00OOO0 .finalX )/O00OO0OO0OO00OOO0 .finalY #line:525
def YesOrNo (O00O0O00OOO000000 ):#line:527
    global flg ,fff ,f #line:528
    if flg !=1 and O00O0O00OOO000000 .distanceY >=0 and O00O0O00OOO000000 .distanceY <=300 :#line:529
        lengths (O00O0O00OOO000000 ,2 )#line:530
        O00O0O00OOO000000 .hook .move (290 +O00O0O00OOO000000 .finalX +O00O0O00OOO000000 .distanceX ,58 +O00O0O00OOO000000 .finalY +O00O0O00OOO000000 .distanceY )#line:531
        return 0 ,0 #line:532
    elif flg ==1 and O00O0O00OOO000000 .distanceY >=0 and fff !=1 :#line:533
        f =1 #line:534
        lengths (O00O0O00OOO000000 ,-2 )#line:535
        return 1 ,0 #line:536
    elif flg ==1 and fff ==1 and O00O0O00OOO000000 .distanceY >=0 :#line:537
        f =1 #line:538
        lengths (O00O0O00OOO000000 ,-2 )#line:539
        O00O0O00OOO000000 .hook .move (290 +O00O0O00OOO000000 .finalX +O00O0O00OOO000000 .distanceX ,58 +O00O0O00OOO000000 .finalY +O00O0O00OOO000000 .distanceY )#line:540
        return 0 ,0 #line:541
    else :#line:542
        if fff !=1 :#line:543
            O00O0O00OOO000000 .distanceY =0 #line:544
            flg ,f ,fff ,O00O0O00OOO000000 .isdo =0 ,0 ,0 ,0 #line:545
            return 1 ,1 #line:546
        O00O0O00OOO000000 .distanceY =0 #line:547
        flg ,f ,fff ,O00O0O00OOO000000 .isdo =0 ,0 ,0 ,0 #line:548
        O00O0O00OOO000000 .elderGif .stop ()#line:549
        print (12 )#line:550
        return 0 ,0 #line:551
def playAudio (O0O0O0OO0000OOO0O ):#line:553
    O0O0OO0O0O0OO0OOO =PyQt5_QMediaPlayer ()#line:554
    O0O0OO0O0O0OO0OOO .prepare_audio (O0O0O0OO0000OOO0O )#line:555
    O0O0OO0O0O0OO0OOO .play ()#line:556
def change_img (O00OOOOOOOO00O000 ,OO00O00OOO000OO00 ,OO000O0OOO0OO0000 ,OO000OO000OO0O000 ):#line:558
    if O00OOOOOOOO00O000 .namelist [O00OOOOOOOO00O000 .index ][1 ]==OO00O00OOO000OO00 :#line:559
        O00OOOOOOOO00O000 .namelist [O00OOOOOOOO00O000 .index ][0 ].setBackground ("hook_gold.png")#line:560
    elif O00OOOOOOOO00O000 .namelist [O00OOOOOOOO00O000 .index ][1 ]==OO000O0OOO0OO0000 :#line:561
        O00OOOOOOOO00O000 .namelist [O00OOOOOOOO00O000 .index ][0 ].setBackground ("hook_diamond.png")#line:562
    else :#line:563
        O00OOOOOOOO00O000 .namelist [O00OOOOOOOO00O000 .index ][0 ].setBackground ("hook_stone.png")#line:564
def getBorder ():#line:566
    return borderr #line:567

name="VipCode"