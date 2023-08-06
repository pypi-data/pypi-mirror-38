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

parwidth =600 #line:1
flg =0 #line:3
fff =0 #line:4
f =0 #line:5
border =0 #line:6
borderr =0 #line:7
angle =1 #line:8
direction =1 #line:9
ipStr ='http://jiaoxue.vipcode.cn/'#line:11
global filename #line:13
filename =""#line:14
class PyQt5_QDialog (QDialog ):#line:17
    def __init__ (O0O00OOO00000OOOO ):#line:18
        super ().__init__ ()#line:19
        O0O00OOO00000OOOO .setObjectName ("dialog")#line:20
        global parwidth #line:21
        parwidth =O0O00OOO00000OOOO .width ()+200 #line:22
    def setBackgroundColor (O0000000O00OO00O0 ,O0OOOO00O0O0000OO ):#line:23
        O0000000O00OO00O0 .setStyleSheet ("#dialog{background-color:"+O0OOOO00O0O0000OO +"}")#line:24
    def setBackground (O00O00OO0OOOOOO0O ,O000OO00O000O0O0O ):#line:25
        O00O00OO0OOOOOO0O .setStyleSheet ("#dialog{border-image:url(RESOURCE/drawable/"+O000OO00O000O0O0O +")}")#line:26
    def setResize (O000O00OO000OO000 ,O0O0OOOO0OOO000O0 ,OOOOOO000O000OO00 ):#line:28
        O000O00OO000OO000 .resize (O0O0OOOO0OOO000O0 ,OOOOOO000O000OO00 )#line:29
    def addBodyButton (O0000OOO0OOOOOO00 ,O0000O0000OO0OO00 ):#line:31
        O0000OOO0OOOOOO00 .bodylabel =O0000O0000OO0OO00 #line:32
        O0000OOO0OOOOOO00 .head =PyQt5_QPushButton (O0000OOO0OOOOOO00 ,400 ,300 ,160 ,130 )#line:33
        O0000OOO0OOOOOO00 .head .setBackgroundColor ("rgba(100,0, 200, 0)")#line:34
        O0000OOO0OOOOOO00 .body =PyQt5_QPushButton (O0000OOO0OOOOOO00 ,445 ,430 ,70 ,80 )#line:36
        O0000OOO0OOOOOO00 .body .setBackgroundColor ("rgba(100,0, 200, 0)")#line:37
        O0000OOO0OOOOOO00 .leftArm =PyQt5_QPushButton (O0000OOO0OOOOOO00 ,420 ,430 ,40 ,30 )#line:39
        O0000OOO0OOOOOO00 .leftArm .setBackgroundColor ("rgba(0,0, 0, 0)")#line:40
        O0000OOO0OOOOOO00 .rightArm =PyQt5_QPushButton (O0000OOO0OOOOOO00 ,505 ,430 ,50 ,30 )#line:42
        O0000OOO0OOOOOO00 .rightArm .setBackgroundColor ("rgba(0,0, 0, 0)")#line:43
        O0000OOO0OOOOOO00 .leftFoot =PyQt5_QPushButton (O0000OOO0OOOOOO00 ,440 ,500 ,30 ,30 )#line:45
        O0000OOO0OOOOOO00 .leftFoot .setBackgroundColor ("rgba(0,0, 0, 0)")#line:46
        O0000OOO0OOOOOO00 .rightFoot =PyQt5_QPushButton (O0000OOO0OOOOOO00 ,500 ,500 ,30 ,30 )#line:48
        O0000OOO0OOOOOO00 .rightFoot .setBackgroundColor ("rgba(0,0, 0, 0)")#line:49
        O0000OOO0OOOOOO00 .head .clicked .connect (O0000OOO0OOOOOO00 .headClicked )#line:51
        O0000OOO0OOOOOO00 .leftArm .clicked .connect (O0000OOO0OOOOOO00 .armClicked )#line:52
        O0000OOO0OOOOOO00 .rightArm .clicked .connect (O0000OOO0OOOOOO00 .armClicked )#line:53
        O0000OOO0OOOOOO00 .rightFoot .clicked .connect (O0000OOO0OOOOOO00 .rightFootClicked )#line:54
        O0000OOO0OOOOOO00 .leftFoot .clicked .connect (O0000OOO0OOOOOO00 .leftFootClicked )#line:55
        O0000OOO0OOOOOO00 .body .clicked .connect (O0000OOO0OOOOOO00 .bodyClicked )#line:56
    def armClicked (O0O00O0OO0O0O0000 ):#line:57
        O0O00O0OO0O0O0000 .neibu2 ('main_arm')#line:58
        O0O00O0OO0O0O0000 .neibu1 ('main_arm')#line:63
    def leftFootClicked (O0O00000000O000OO ):#line:64
        O0O00000000O000OO .neibu2 ('main_leftFoot')#line:65
        O0O00000000O000OO .neibu1 ('main_leftFoot')#line:66
    def rightFootClicked (OO0OO000OOOO0O00O ):#line:67
        OO0OO000OOOO0O00O .neibu2 ('main_rightFoot')#line:68
        OO0OO000OOOO0O00O .neibu1 ('main_rightFoot')#line:69
    def bodyClicked (OOO00O0OO00O00000 ):#line:70
        OOO00O0OO00O00000 .neibu2 ('main_body')#line:71
        OOO00O0OO00O00000 .neibu1 ('main_body')#line:72
    def headClicked (O0O00OO000OO0OO0O ):#line:73
        O0O00OO000OO0OO0O .neibu2 ('main_head')#line:74
        O0O00OO000OO0OO0O .neibu1 ('main_head')#line:75
    def neibu2 (OO00O0OO00OOO0O00 ,O0OOO0000O00OO0O0 ):#line:77
        OO00O0OO00OOO0O00 .neigif =PyQt5_QMovie (O0OOO0000O00OO0O0 +'.gif')#line:79
        OO00O0OO00OOO0O00 .neigif .setScaledSize (OO00O0OO00OOO0O00 .bodylabel .size ())#line:81
        OO00O0OO00OOO0O00 .bodylabel .setMovie (OO00O0OO00OOO0O00 .neigif )#line:83
        OO00O0OO00OOO0O00 .neigif .start ()#line:85
        OO00O0OO00OOO0O00 .frameCount =OO00O0OO00OOO0O00 .neigif .frameCount ()#line:86
        OO00O0OO00OOO0O00 .neigif .frameChanged .connect (OO00O0OO00OOO0O00 .neibu3 )#line:88
    def neibu3 (O0O0O0OOOO00OO0OO ):#line:89
        O0O0O0OOOO00OO0OO .frameCount -=1 #line:91
        if O0O0O0OOOO00OO0OO .frameCount ==0 :#line:93
            O0O0O0OOOO00OO0OO .neigif .stop ()#line:95
            O0O0O0OOOO00OO0OO .neigif =PyQt5_QMovie ('main_lion.gif')#line:97
            O0O0O0OOOO00OO0OO .neigif .setScaledSize (O0O0O0OOOO00OO0OO .bodylabel .size ())#line:98
            O0O0O0OOOO00OO0OO .bodylabel .setMovie (O0O0O0OOOO00OO0OO .neigif )#line:100
            O0O0O0OOOO00OO0OO .neigif .start ()#line:102
    def neibu1 (OOO0O00OOOO0OO0OO ,O0OO00OOOOOO0OO00 ):#line:104
        O00O000O000000000 =PyQt5_QMediaPlayer ()#line:106
        O00O000O000000000 .prepare_audio (O0OO00OOOOOO0OO00 +'.wav')#line:108
        O00O000O000000000 .play ()#line:110
class PyQt5_QPushButton (QPushButton ):#line:113
    def __init__ (O00OOO0O0O0O000O0 ,O0O0OO0O0O00OO0O0 ,x =0 ,y =0 ,width =113 ,height =32 ):#line:114
        super ().__init__ (O0O0OO0O0O00OO0O0 )#line:115
        O00OOO0O0O0O000O0 .setGeometry (x ,y ,width ,height )#line:116
    def setBackground (O000O0OOOOO0OOO00 ,O0OOOO00OOO0O00O0 ):#line:118
        O000O0OOOOO0OOO00 .setStyleSheet (O000O0OOOOO0OOO00 .styleSheet ()+"QPushButton{border-image:url(RESOURCE/drawable/"+O0OOOO00OOO0O00O0 +")}")#line:120
    def setPressedBackground (OOOO000O0OOOO00O0 ,O00O0OOO00O0O00O0 ):#line:122
        OOOO000O0OOOO00O0 .setStyleSheet (OOOO000O0OOOO00O0 .styleSheet ()+"QPushButton:pressed{border-image:url(RESOURCE/drawable/"+O00O0OOO00O0O00O0 +")}")#line:124
    def setBackgroundColor (O00O000OO00O0O00O ,O0OOO0OOO0O00O00O ):#line:126
        O00O000OO00O0O00O .setStyleSheet (O00O000OO00O0O00O .styleSheet ()+"QPushButton{background-color:"+O0OOO0OOO0O00O00O +"}")#line:127
    def setTextColor (OOOOO0O0O000OO0O0 ,OOOOO0000000OO00O ):#line:129
        OOOOO0O0O000OO0O0 .setStyleSheet (OOOOO0O0O000OO0O0 .styleSheet ()+"QPushButton{color:"+OOOOO0000000OO00O +"}")#line:130
    def setPressedTextColor (OOO00OO00OOOOOOO0 ,OO0000000OO0O0OOO ):#line:132
        OOO00OO00OOOOOOO0 .setStyleSheet (OOO00OO00OOOOOOO0 .styleSheet ()+"QPushButton:pressed{color:"+OO0000000OO0O0OOO +"}")#line:133
    def setFontSize (OO00OO0OOOO0OO00O ,O0OO0OO00O00OO000 ):#line:135
        OOO0O000000O0O00O =QFont ()#line:136
        OOO0O000000O0O00O .setPixelSize (O0OO0OO00O00OO000 )#line:137
        OO00OO0OOOO0OO00O .setFont (OOO0O000000O0O00O )#line:138
class PyQt5_QLineEdit (QLineEdit ):#line:141
    Password =QLineEdit .Password #line:142
    Normal =QLineEdit .Normal #line:143
    NoEcho =QLineEdit .NoEcho #line:144
    PasswordEchoOnEdit =QLineEdit .PasswordEchoOnEdit #line:145
    def __init__ (OO00O0OOOOOO0000O ,O0OO00OOOO0O00O00 ,x =0 ,y =0 ,width =113 ,height =21 ):#line:147
        super ().__init__ (O0OO00OOOO0O00O00 )#line:148
        OO00O0OOOOOO0000O .setGeometry (x ,y ,width ,height )#line:149
        OO00O0OOOOOO0000O .setFontSize (14 )#line:150
        OO00O0OOOOOO0000O .setAlignment (Qt .AlignVCenter )#line:151
    def setFontSize (O0O00OOOOOO0000OO ,OO0O0OO0000OO00OO ):#line:153
        OOO0O0O00OO00O00O =QFont ()#line:154
        OOO0O0O00OO00O00O .setPixelSize (OO0O0OO0000OO00OO )#line:155
        O0O00OOOOOO0000OO .setFont (OOO0O0O00OO00O00O )#line:156
    def setBackground (O0O000OO0O00000OO ,OO0OOOOOOO00OO0OO ):#line:158
        O0O000OO0O00000OO .setStyleSheet (O0O000OO0O00000OO .styleSheet ()+"border-image:url(RESOURCE/drawable/"+OO0OOOOOOO00OO0OO +");")#line:159
    def setBackgroundColor (OO0OOOO00O0OOOOOO ,O0O0OOOOO00O00O0O ):#line:161
        OO0OOOO00O0OOOOOO .setStyleSheet (OO0OOOO00O0OOOOOO .styleSheet ()+"background-color:"+O0O0OOOOO00O00O0O +";")#line:162
    def setTextColor (O0O0O000OO000OO0O ,OOOOOOOOOO0OO0000 ):#line:164
        O0O0O000OO000OO0O .setStyleSheet (O0O0O000OO000OO0O .styleSheet ()+"color:"+OOOOOOOOOO0OO0000 +";")#line:165
    def setDisplayMode (O0O0000O000OOO000 ,OOOO000O0O00O00OO ):#line:167
        if OOOO000O0O00O00OO ==PyQt5_QLineEdit .Password :#line:168
            O0O0000O000OOO000 .setEchoMode (OOOO000O0O00O00OO )#line:169
        elif OOOO000O0O00O00OO ==PyQt5_QLineEdit .Normal :#line:170
            O0O0000O000OOO000 .setEchoMode (OOOO000O0O00O00OO )#line:171
        elif OOOO000O0O00O00OO ==PyQt5_QLineEdit .NoEcho :#line:172
            O0O0000O000OOO000 .setEchoMode (OOOO000O0O00O00OO )#line:173
        elif OOOO000O0O00O00OO ==PyQt5_QLineEdit .PasswordEchoOnEdit :#line:174
            O0O0000O000OOO000 .setEchoMode (OOOO000O0O00O00OO )#line:175
class PyQt5_Qlabel (QLabel ):#line:178
    clicked =pyqtSignal (QMouseEvent )#line:179
    def __init__ (OO000000000000OOO ,OOO0000OO0OO000OO ,x =0 ,y =0 ,width =60 ,height =16 ):#line:180
        super ().__init__ (OOO0000OO0OO000OO )#line:181
        OO000000000000OOO .widget =OOO0000OO0OO000OO #line:182
        OO000000000000OOO .zeze =True #line:183
        OO000000000000OOO .setGeometry (x ,y ,width ,height )#line:184
    def setFontSize (OOO000OOO00OOOO00 ,O0O0OO0O0OO0O00OO ):#line:185
        OO00OO0O0OO0OO00O =QFont ()#line:186
        OO00OO0O0OO0OO00O .setPixelSize (O0O0OO0O0OO0O00OO )#line:187
        OOO000OOO00OOOO00 .setFont (OO00OO0O0OO0OO00O )#line:188
    def setFontFitSize (OOO00000OOOOOO0OO ,O0O0000O0OOOOO00O ):#line:189
        O0OO00OOOOO0O0OOO =QFont ()#line:190
        O0OO00OOOOO0O0OOO .setPointSize (O0O0000O0OOOOO00O )#line:191
        OOO00000OOOOOO0OO .setFont (O0OO00OOOOO0O0OOO )#line:192
    def setBackground (OO0OO00OOOO000000 ,OO0OO00000O0000O0 ):#line:193
        OO0OO00OOOO000000 .setStyleSheet (OO0OO00OOOO000000 .styleSheet ()+"border-image:url(RESOURCE/drawable/"+OO0OO00000O0000O0 +");")#line:194
    def setBackgroundColor (OOOO0O00O0O00OO00 ,OOO0O00OOOO0OOO0O ):#line:196
        OOOO0O00O0O00OO00 .setStyleSheet (OOOO0O00O0O00OO00 .styleSheet ()+"background-color:"+OOO0O00OOOO0OOO0O +";")#line:197
    def setTextColor (OOO00O00OO0O0O0O0 ,OO00OOO0OO0OOOO0O ):#line:199
        OOO00O00OO0O0O0O0 .setStyleSheet (OOO00O00OO0O0O0O0 .styleSheet ()+"color:"+OO00OOO0OO0OOOO0O +";")#line:200
    def mouseReleaseEvent (O00O0O000000O0O00 ,OO00OO0OO00O00OOO ):#line:201
        O00O0O000000O0O00 .released .emit (OO00OO0OO00O00OOO )#line:202
    released =pyqtSignal (QMouseEvent )#line:203
    pressed =pyqtSignal (QEvent )#line:204
    def mousePressEvent (O0OO000O0O0OOOOO0 ,O0O000OOO00OOO0O0 ):#line:205
        O0OO000O0O0OOOOO0 .pressed .emit (O0O000OOO00OOO0O0 )#line:206
        if O0O000OOO00OOO0O0 .buttons ()==Qt .LeftButton :#line:207
            O0OO000O0O0OOOOO0 .clicked .emit (O0O000OOO00OOO0O0 )#line:208
    moved =pyqtSignal (QMouseEvent )#line:209
    def mouseMoveEvent (OO000OOOOOO0OO0OO ,O0OOOOOO0O0O0O0OO ):#line:210
        OO000OOOOOO0OO0OO .moved .emit (O0OOOOOO0O0O0O0OO )#line:211
    doubleclicked =pyqtSignal (QMouseEvent )#line:212
    def mouseDoubleClickEvent (O0OOO00000000000O ,OO0OO0OOO0OO0O0OO ):#line:213
        if OO0OO0OOO0OO0O0OO .buttons ()==Qt .LeftButton :#line:214
            O0OOO00000000000O .doubleclicked .emit (OO0OO0OOO0OO0O0OO )#line:215
    entered =pyqtSignal (QEnterEvent )#line:216
    def enterEvent (OOO00OOOO0O0O0OOO ,O00O0000O0OO0OO0O ):#line:217
        OOO00OOOO0O0O0OOO .entered .emit (O00O0000O0OO0OO0O )#line:218
    leaved =pyqtSignal (QEvent )#line:220
    def leaveEvent (O000O0OOO000OOOOO ,OO0O00OOOOO0OOOOO ):#line:221
        O000O0OOO000OOOOO .leaved .emit (OO0O00OOOOO0OOOOO )#line:222
    def setSize (O0OOOO000OO0OO0O0 ,O00O00OOO0O0OO0OO ):#line:225
        O0OOOO000OO0OO0O0 .setFixedSize (O00O00OOO0O0OO0OO )#line:226
    def refresh (OO00O0O0000000O0O ):#line:227
        if OO00O0O0000000O0O .zeze :#line:228
            OO00O0O0000000O0O .widget .resize (OO00O0O0000000O0O .widget .width ()+1 ,OO00O0O0000000O0O .widget .height ()+1 )#line:229
            OO00O0O0000000O0O .zeze =False #line:230
        else :#line:231
            OO00O0O0000000O0O .widget .resize (OO00O0O0000000O0O .widget .width ()-1 ,OO00O0O0000000O0O .widget .height ()-1 )#line:232
            OO00O0O0000000O0O .zeze =True #line:233
class PyQt5_QMovie (QMovie ):#line:235
    def __init__ (OOO0O0OO00O00OOOO ,OOO0OO000O0O0OO0O ):#line:236
        super ().__init__ ("RESOURCE/gif/"+OOO0OO000O0O0OO0O )#line:237
class PyQt5_QMediaPlayer ():#line:239
    def __init__ (O0O0O0O0O00O0O0O0 ):#line:240
        pygame .mixer .init ()#line:241
        O0O0O0O0O00O0O0O0 .music =pygame .mixer .music #line:242
    def prepare_audio (O00O0000OO00O0OOO ,O00OOOOO0O0O000OO ):#line:243
        O00O0000OO00O0OOO .music .load ("RESOURCE/audio/"+O00OOOOO0O0O000OO )#line:244
    def prepare_voice (OO00O0OOO0OO0OOO0 ,OO00OO0O000O0O0OO ):#line:245
        OO00O0OOO0OO0OOO0 .music .load ("RESOURCE/voice/"+OO00OO0O000O0O0OO )#line:246
    def play (OO000O0OOO000O000 ,loops =1 ,start =0.0 ):#line:247
        if loops ==0 :#line:248
            OO000O0OOO000O000 .music .play (-1 ,start )#line:249
        elif loops <0 :#line:250
            pass #line:251
        elif loops >0 :#line:252
            OO000O0OOO000O000 .music .play (loops -1 ,start )#line:253
    def stop (OOOO0O00OOOOOO0O0 ):#line:254
        OOOO0O00OOOOOO0O0 .music .stop ()#line:255
    def pause (O0O0OO000O0O000OO ):#line:256
        O0O0OO000O0O000OO .music .pause ()#line:257
    def setVolume (O000OOO0OOOO0O00O ,O0O0O0OOOO0OO000O ):#line:258
        O000OOO0OOOO0O00O .music .set_volume (O0O0O0OOOO0OO000O )#line:259
    def isPlaying (O000O00OOOOO00OO0 ):#line:260
        if O000O00OOOOO00OO0 .music .get_busy ()==1 :#line:261
            return True #line:262
        else :#line:263
            return False #line:264
class PyQt5_QCheckBox (QCheckBox ):#line:268
    def __init__ (OOO00O00OOO0OOO00 ,OO0O00O0O0O000O0O ,x =0 ,y =0 ,width =20 ,height =20 ):#line:269
        super ().__init__ (OO0O00O0O0O000O0O )#line:270
        OOO00O00OOO0OOO00 .setGeometry (x ,y ,width ,height )#line:271
        OOO00O00OOO0OOO00 .isIndicator =True #line:272
        OOO00O00OOO0OOO00 .image_name_normal =""#line:273
        OOO00O00OOO0OOO00 .image_name_pressed =""#line:274
    def setIndicator (O000000OOOOOO0O00 ,OO0OOO0000O00000O ):#line:276
        O000000OOOOOO0O00 .isIndicator =OO0OOO0000O00000O #line:277
        O000000OOOOOO0O00 .setStyleSheet ("")#line:278
        if O000000OOOOOO0O00 .image_name_normal !="":#line:279
            O000000OOOOOO0O00 .setUncheckedBackground (O000000OOOOOO0O00 .image_name_normal )#line:280
        if O000000OOOOOO0O00 .image_name_pressed !="":#line:281
            O000000OOOOOO0O00 .setCheckedBackground (O000000OOOOOO0O00 .image_name_pressed )#line:282
    def setUncheckedBackground (O0OO000OO0000O00O ,OO00OO000OOOOOOO0 ):#line:284
        if O0OO000OO0000O00O .isIndicator :#line:285
            O0OO000OO0000O00O .setStyleSheet (O0OO000OO0000O00O .styleSheet ()+"QCheckBox:unchecked{width:"+str (O0OO000OO0000O00O .width ())+"px;height:"+str (O0OO000OO0000O00O .height ())+"px;border-image:url(RESOURCE/drawable/"+OO00OO000OOOOOOO0 +")}")#line:288
        else :#line:289
            O0OO000OO0000O00O .setStyleSheet (O0OO000OO0000O00O .styleSheet ()+"QCheckBox:indicator:unchecked{width:"+str (O0OO000OO0000O00O .width ())+"px;height:"+str (O0OO000OO0000O00O .height ())+"px;border-image:url(RESOURCE/drawable/"+OO00OO000OOOOOOO0 +")}")#line:292
        O0OO000OO0000O00O .image_name_normal =OO00OO000OOOOOOO0 #line:293
    def setCheckedBackground (O00O0OOOOO00OOO00 ,OO000O0O0000OOOO0 ):#line:295
        if O00O0OOOOO00OOO00 .isIndicator :#line:296
            O00O0OOOOO00OOO00 .setStyleSheet (O00O0OOOOO00OOO00 .styleSheet ()+"QCheckBox:checked{width:"+str (O00O0OOOOO00OOO00 .width ())+"px;height:"+str (O00O0OOOOO00OOO00 .height ())+"px;border-image:url(RESOURCE/drawable/"+OO000O0O0000OOOO0 +")}")#line:299
        else :#line:300
            O00O0OOOOO00OOO00 .setStyleSheet (O00O0OOOOO00OOO00 .styleSheet ()+"QCheckBox:indicator:checked{width:"+str (O00O0OOOOO00OOO00 .width ())+"px;height:"+str (O00O0OOOOO00OOO00 .height ())+"px;border-image:url(RESOURCE/drawable/"+OO000O0O0000OOOO0 +")}")#line:303
        O00O0OOOOO00OOO00 .image_name_pressed =OO000O0O0000OOOO0 #line:304
class PyQt5_QRadioButton (QRadioButton ):#line:307
    def __init__ (O0O0O0000O0OOOO0O ,O00OO0OOO0O0OO0OO ,x =0 ,y =0 ,width =20 ,height =20 ):#line:308
        super ().__init__ (O00OO0OOO0O0OO0OO )#line:309
        O0O0O0000O0OOOO0O .setGeometry (x ,y ,width ,height )#line:310
        O0O0O0000O0OOOO0O .isIndicator =True #line:311
        O0O0O0000O0OOOO0O .image_name_normal =""#line:312
        O0O0O0000O0OOOO0O .image_name_pressed =""#line:313
    def setFontSize (O000000O0O0O0O0O0 ,OO0O000OO0OO0O000 ):#line:315
        OOO000OO0O0O0OOO0 =QFont ()#line:316
        OOO000OO0O0O0OOO0 .setPixelSize (OO0O000OO0OO0O000 )#line:317
        O000000O0O0O0O0O0 .setFont (OOO000OO0O0O0OOO0 )#line:318
    def setTextColor (OOO0OO00O0O00O0O0 ,OOOO0O0000OOOOO0O ):#line:320
        OOO0OO00O0O00O0O0 .setStyleSheet (OOO0OO00O0O00O0O0 .styleSheet ()+"color:"+OOOO0O0000OOOOO0O +";")#line:321
    def setIndicator (O00OO000OOOOOOO0O ,O0000OO0O0O000O0O ):#line:323
        O00OO000OOOOOOO0O .isIndicator =O0000OO0O0O000O0O #line:324
        O00OO000OOOOOOO0O .setStyleSheet ("")#line:325
        if O00OO000OOOOOOO0O .image_name_normal !="":#line:326
            O00OO000OOOOOOO0O .setUncheckedBackground (O00OO000OOOOOOO0O .image_name_normal )#line:327
        if O00OO000OOOOOOO0O .image_name_pressed !="":#line:328
            O00OO000OOOOOOO0O .setCheckedBackground (O00OO000OOOOOOO0O .image_name_pressed )#line:329
    def setUncheckedBackground (OO00O0OOOO0O0OO00 ,OOOO0O00OOO000O00 ):#line:331
        if OO00O0OOOO0O0OO00 .isIndicator :#line:332
            OO00O0OOOO0O0OO00 .setStyleSheet (OO00O0OOOO0O0OO00 .styleSheet ()+"QRadioButton:unchecked{width:"+str (OO00O0OOOO0O0OO00 .width ())+"px;height:"+str (OO00O0OOOO0O0OO00 .height ())+"px;border-image:url(RESOURCE/drawable/"+OOOO0O00OOO000O00 +")}")#line:335
        else :#line:336
            OO00O0OOOO0O0OO00 .setStyleSheet (OO00O0OOOO0O0OO00 .styleSheet ()+"QRadioButton:indicator:unchecked{width:"+str (OO00O0OOOO0O0OO00 .width ())+"px;height:"+str (OO00O0OOOO0O0OO00 .height ())+"px;border-image:url(RESOURCE/drawable/"+OOOO0O00OOO000O00 +")}")#line:339
        OO00O0OOOO0O0OO00 .image_name_normal =OOOO0O00OOO000O00 #line:340
    def setCheckedBackground (O0OO000O000OOOOO0 ,O00O0OOOO0O0OOOO0 ):#line:342
        if O0OO000O000OOOOO0 .isIndicator :#line:343
            O0OO000O000OOOOO0 .setStyleSheet (O0OO000O000OOOOO0 .styleSheet ()+"QRadioButton:checked{width:"+str (O0OO000O000OOOOO0 .width ())+"px;height:"+str (O0OO000O000OOOOO0 .height ())+"px;border-image:url(RESOURCE/drawable/"+O00O0OOOO0O0OOOO0 +")}")#line:346
        else :#line:347
            O0OO000O000OOOOO0 .setStyleSheet (O0OO000O000OOOOO0 .styleSheet ()+"QRadioButton:indicator:checked{width:"+str (O0OO000O000OOOOO0 .width ())+"px;height:"+str (O0OO000O000OOOOO0 .height ())+"px;border-image:url(RESOURCE/drawable/"+O00O0OOOO0O0OOOO0 +")}")#line:350
        O0OO000O000OOOOO0 .image_name_pressed =O00O0OOOO0O0OOOO0 #line:351
class PyQt5_QGroupBox (QGroupBox ):#line:354
    def __init__ (O000OOOOO0O0O00O0 ,OO00O0O000O00OOO0 ,x =0 ,y =0 ,width =120 ,height =80 ):#line:355
        super ().__init__ (OO00O0O000O00OOO0 )#line:356
        O000OOOOO0O0O00O0 .setGeometry (x ,y ,width ,height )#line:357
        O000OOOOO0O0O00O0 .setObjectName ("groupbox")#line:358
    def setBackground (OOO0OO00000OO00O0 ,OOO00OOO0OO00OO00 ):#line:360
        OOO0OO00000OO00O0 .setStyleSheet ("#groupbox{border-image:url(RESOURCE/drawable/"+OOO00OOO0OO00OO00 +")}")#line:361
    def setBackgroundColor (O000OO0OOO0O0OO00 ,O00000O00O0OOOOOO ):#line:363
        O000OO0OOO0O0OO00 .setStyleSheet ("#groupbox{background-color:"+O00000O00O0OOOOOO +"}")#line:364
    def setBorderWidth (OOO0O0OO0O00OO000 ,OO0O0OOO00OOOO0O0 ):#line:366
        OOO0O0OO0O00OO000 .setStyleSheet (OOO0O0OO0O00OO000 .styleSheet ()+"border-width:"+str (OO0O0OOO00OOOO0O0 )+"px;border-style:solid;")#line:367
def getQuestion (OO00000O0O0O0O00O ):#line:370
    try :#line:371
        OO00OO000O0000O00 =ipStr +'ti/findById.do?id=%d'%OO00000O0O0O0O00O #line:373
        OO00OO000O0000O00 =urllib .request .Request (url =OO00OO000O0000O00 )#line:374
        OO00OO000O0000O00 .add_header ('Content-Type','application/json')#line:375
        O00OO00OO00O0OOO0 =urllib .request .urlopen (OO00OO000O0000O00 )#line:376
    except urllib .error .URLError as OO0OOOOOO00OO0O0O :#line:377
        OOOOOOO0O0OO0O0O0 ={"id":1 ,"wenti":"由于网络问题未找到所需内容，请检查您的网络","daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:378
        return OOOOOOO0O0OO0O0O0 #line:379
    OOOOOOO0O0OO0O0O0 =json .loads (O00OO00OO00O0OOO0 .read ().decode ('utf-8'))#line:381
    if OOOOOOO0O0OO0O0O0 :#line:383
        if OOOOOOO0O0OO0O0O0 ["state"]!=0 :#line:384
            return {"id":1 ,"wenti":OOOOOOO0O0OO0O0O0 ["message"],"daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:385
        else :#line:386
            return OOOOOOO0O0OO0O0O0 ["data"]#line:387
def reductionRadioBtn (OO000O0OO0OOO0000 ):#line:388
    for O0OO000OO0O0OOO00 in range (len (OO000O0OO0OOO0000 )):#line:389
        OO000O0OO0OOO0000 [O0OO000OO0O0OOO00 ].setCheckable (False )#line:390
        OO000O0OO0OOO0000 [O0OO000OO0O0OOO00 ].setCheckable (True )#line:391
class PyQt5_QSystemTrayIcon (QSystemTrayIcon ):#line:392
    def __init__ (O0OOOOOO0O0000O00 ,parent =None ):#line:393
        super (PyQt5_QSystemTrayIcon ,O0OOOOOO0O0000O00 ).__init__ (parent )#line:394
        O0OOOOOO0O0000O00 .menu =QMenu ()#line:395
        O0OOOOOO0O0000O00 .setContextMenu (O0OOOOOO0O0000O00 .menu )#line:396
    def addMenu (O00OO00O000OOOOOO ,O0O0OOOO0OO0O00O0 ):#line:397
        O00OO00O000OOOOOO .menuAction =QAction (O0O0OOOO0OO0O00O0 ,O00OO00O000OOOOOO )#line:398
        O00OO00O000OOOOOO .menu .addAction (O00OO00O000OOOOOO .menuAction )#line:399
        return O00OO00O000OOOOOO .menuAction #line:400
    def _setIcon (OO0O000OOOOOO0000 ,O0OO0OOOO00000O00 ):#line:401
        OO0O000OOOOOO0000 .setIcon (QIcon ("RESOURCE/drawable/"+O0OO0OOOO00000O00 ))#line:402
class PyQt5_Animation (QPropertyAnimation ):#line:405
    animFinished =pyqtSignal ()#line:406
    def __init__ (OO000O000O0O00O00 ,QWidget =None ):#line:407
        super (PyQt5_Animation ,OO000O000O0O00O00 ).__init__ ()#line:408
        OO000O000O0O00O00 .setPropertyName (b"geometry")#line:409
        OO000O000O0O00O00 .setTargetObject (QWidget )#line:410
        OO000O000O0O00O00 .finished .connect (OO000O000O0O00O00 .aFinished )#line:411
        OO000O000O0O00O00 .widget =QWidget #line:412
        OO000O000O0O00O00 .valueChanged .connect (OO000O000O0O00O00 .up )#line:413
        OO000O000O0O00O00 .ze =True #line:414
    def up (O00OOO0OOOOO0OOOO ):#line:415
        if O00OOO0OOOOO0OOOO .ze :#line:416
            O00OOO0OOOOO0OOOO .widget .resize (O00OOO0OOOOO0OOOO .widget .width ()+1 ,O00OOO0OOOOO0OOOO .widget .height ()+1 )#line:417
            O00OOO0OOOOO0OOOO .ze =False #line:418
        else :#line:419
            O00OOO0OOOOO0OOOO .widget .resize (O00OOO0OOOOO0OOOO .widget .width ()-1 ,O00OOO0OOOOO0OOOO .widget .height ()-1 )#line:420
            O00OOO0OOOOO0OOOO .ze =True #line:421
    def setStartValues (O0O00000OO0O0O0OO ,O00000O00O0O0O00O ,OOOOOOOO0000O000O ,OO0OO00OO0OOOO0OO ,O0O0O0O0OOO0OO000 ):#line:423
        O0O00000OO0O0O0OO .setStartValue (QRect (O00000O00O0O0O00O ,OOOOOOOO0000O000O ,OO0OO00OO0OOOO0OO ,O0O0O0O0OOO0OO000 ))#line:424
    def setEndValues (OO0OOO0O0OOO0000O ,OO00OO00O0OOOOOOO ,OO0OOO000O0O0OOOO ,O00O0O0O0O00000OO ,OOO0O0OOO00O0000O ):#line:425
        OO0OOO0O0OOO0000O .setEndValue (QRect (OO00OO00O0OOOOOOO ,OO0OOO000O0O0OOOO ,O00O0O0O0O00000OO ,OOO0O0OOO00O0000O ))#line:426
    def setMode (O00O00OO00O0OO0OO ,OO0O0OO0000O0OOO0 ):#line:427
        O00O00OO00O0OO0OO .setEasingCurve (OO0O0OO0000O0OOO0 )#line:428
    def aFinished (O0OO0O0O0OOOOO0O0 ):#line:429
        O0OO0O0O0OOOOO0O0 .animFinished .emit ()#line:430
class Mode ():#line:432
    InOut =QEasingCurve .InOutBack #line:434
    OutIn =QEasingCurve .OutInBack #line:435
    InZero =QEasingCurve .InQuart #line:437
    OutZero =QEasingCurve .OutQuart #line:438
    InElastic =QEasingCurve .InElastic #line:440
    OutElastic =QEasingCurve .OutElastic #line:441
    InBounce =QEasingCurve .InBounce #line:443
    OutBounce =QEasingCurve .OutBounce #line:444
class PyQt5_FramelessBox (QDialog ):#line:446
    def __init__ (OOOOOOOOO00OOOO00 ):#line:447
        super ().__init__ ()#line:448
        OOOOOOOOO00OOOO00 .resize (340 ,340 )#line:449
        OOOOOOOOO00OOOO00 .setObjectName ("FramelessBox")#line:450
        OOOOOOOOO00OOOO00 .setWindowFlags (OOOOOOOOO00OOOO00 .windowFlags ()|Qt .FramelessWindowHint )#line:451
    def setWindowsTop (O00OOOO00O0OOOO00 ,O00OO0O0O0O00000O ):#line:453
        if O00OO0O0O0O00000O :#line:454
            O00OOOO00O0OOOO00 .setWindowFlags (O00OOOO00O0OOOO00 .windowFlags ()|Qt .WindowStaysOnTopHint )#line:455
    def setResize (O0OO0OO00O00O0O0O ,O00OOOOO0OO0O00O0 ,O00OOOOO0OO0O0OOO ):#line:456
        O0OO0OO00O00O0O0O .resize (O00OOOOO0OO0O00O0 ,O00OOOOO0OO0O0OOO )#line:457
    def setWindowsTransparent (O0O0OOOO0OO0OO0O0 ,OO000OOOOO000O00O ):#line:458
        if OO000OOOOO000O00O :#line:459
            O0O0OOOO0OO0OO0O0 .setAttribute (Qt .WA_TranslucentBackground ,True )#line:460
def getDesktopWidth ():#line:462
    return QApplication .desktop ().width ()#line:463
def getDesktopHeight ():#line:465
    return QApplication .desktop ().height ()#line:466
def rock (O00OOO000O0O0000O ,OO000OO00O0OOOO00 ):#line:468
    global angle ,direction #line:469
    OO0OO0O0OO00OO000 =OO000OO00O0OOOO00 *math .sin (angle )#line:470
    O00O00O0OO0O0O0OO =OO000OO00O0OOOO00 *math .cos (angle )#line:471
    if direction ==1 :#line:472
        if angle <=1 :#line:473
            angle +=0.15 #line:474
        else :#line:475
            direction =-1 #line:476
    if direction ==-1 :#line:477
        if angle >=-1 :#line:478
            angle -=0.15 #line:479
        else :#line:480
            direction =1 #line:481
    O00OOO000O0O0000O .finalX =OO0OO0O0OO00OO000 #line:482
    O00OOO000O0O0000O .finalY =O00O00O0OO0O0O0OO #line:483
def refresh (OOOO00OOO000OOO0O ,OO0O0OO0OO00O0O00 ):#line:485
    for O000OO00000OOO0OO in range (OO0O0OO0OO00O0O00 ):#line:486
        OOOO00OOO000OOO0O .update ()#line:487
        time .sleep (0.01 )#line:488
def judge (O0000OOO0OOO000OO ,OO0OOOOO0O0O0O0OO ,OOO0O00O0000OO00O ,O0OOO00O00OO00000 ,OO0O0O00O000O0OO0 ,OOOOOO0000000O00O ,OO00OO00OOO00O000 ,OO0O000OO0OO00OO0 ,O00O00OO000O0000O ):#line:490
    global flg ,fff ,f ,border ,borderr #line:491
    if f ==1 :#line:492
        flg =1 #line:493
    for OOO00O0O0O000O0O0 in range (len (O0000OOO0OOO000OO .listXY )):#line:494
        if O0000OOO0OOO000OO .namelist [OOO00O0O0O000O0O0 ][1 ]==O0OOO00O00OO00000 :#line:495
            border =OO00OO00OOO00O000 #line:496
        elif O0000OOO0OOO000OO .namelist [OOO00O0O0O000O0O0 ][1 ]==OO0O0O00O000O0OO0 :#line:497
            border =OO0O000OO0OO00OO0 #line:498
        elif O0000OOO0OOO000OO .namelist [OOO00O0O0O000O0O0 ][1 ]==OOOOOO0000000O00O :#line:499
            border =O00O00OO000O0000O #line:500
        if OO0OOOOO0O0O0O0OO >=O0000OOO0OOO000OO .listXY [OOO00O0O0O000O0O0 ][0 ]-5 and OO0OOOOO0O0O0O0OO <=O0000OOO0OOO000OO .listXY [OOO00O0O0O000O0O0 ][0 ]+border +5 :#line:501
            if OOO0O00O0000OO00O >=O0000OOO0OOO000OO .listXY [OOO00O0O0O000O0O0 ][1 ]and OOO0O00O0000OO00O <=O0000OOO0OOO000OO .listXY [OOO00O0O0O000O0O0 ][1 ]+border :#line:502
                borderr =border #line:503
                O0000OOO0OOO000OO .index =OOO00O0O0O000O0O0 #line:504
                print ("碰到了")#line:505
                flg =1 #line:506
    if O0000OOO0OOO000OO .distanceY >300 :#line:507
        fff =1 #line:508
        flg =1 #line:509
def lengths (OOOO0O000O00O0OOO ,O0OO00OO0OO0O0000 ):#line:511
    OOOO0O000O00O0OOO .distanceY +=O0OO00OO0OO0O0000 #line:512
    OOOO0O000O00O0OOO .distanceX +=(O0OO00OO0OO0O0000 *OOOO0O000O00O0OOO .finalX )/OOOO0O000O00O0OOO .finalY #line:513
def YesOrNo (O0OOOO000O0O000O0 ):#line:515
    global flg ,fff ,f #line:516
    if flg !=1 and O0OOOO000O0O000O0 .distanceY >=0 and O0OOOO000O0O000O0 .distanceY <=300 :#line:517
        lengths (O0OOOO000O0O000O0 ,2 )#line:518
        O0OOOO000O0O000O0 .hook .move (290 +O0OOOO000O0O000O0 .finalX +O0OOOO000O0O000O0 .distanceX ,58 +O0OOOO000O0O000O0 .finalY +O0OOOO000O0O000O0 .distanceY )#line:519
        return 0 ,0 #line:520
    elif flg ==1 and O0OOOO000O0O000O0 .distanceY >=0 and fff !=1 :#line:521
        f =1 #line:522
        lengths (O0OOOO000O0O000O0 ,-2 )#line:523
        return 1 ,0 #line:524
    elif flg ==1 and fff ==1 and O0OOOO000O0O000O0 .distanceY >=0 :#line:525
        f =1 #line:526
        lengths (O0OOOO000O0O000O0 ,-2 )#line:527
        O0OOOO000O0O000O0 .hook .move (290 +O0OOOO000O0O000O0 .finalX +O0OOOO000O0O000O0 .distanceX ,58 +O0OOOO000O0O000O0 .finalY +O0OOOO000O0O000O0 .distanceY )#line:528
        return 0 ,0 #line:529
    else :#line:530
        if fff !=1 :#line:531
            O0OOOO000O0O000O0 .distanceY =0 #line:532
            flg ,f ,fff ,O0OOOO000O0O000O0 .isdo =0 ,0 ,0 ,0 #line:533
            return 1 ,1 #line:534
        O0OOOO000O0O000O0 .distanceY =0 #line:535
        flg ,f ,fff ,O0OOOO000O0O000O0 .isdo =0 ,0 ,0 ,0 #line:536
        return 0 ,0 #line:537
def playAudio (OO000O0O0000OO00O ):#line:539
    OOO00O0O00000OOO0 =PyQt5_QMediaPlayer ()#line:540
    OOO00O0O00000OOO0 .prepare_audio (OO000O0O0000OO00O )#line:541
    OOO00O0O00000OOO0 .play ()#line:542
def change_img (OOOOOO00O0OO0000O ,O00000OO000O0OOO0 ,O000OOO0OO000O00O ,OOOOOOOO0OO0OOOOO ):#line:544
    if OOOOOO00O0OO0000O .namelist [OOOOOO00O0OO0000O .index ][1 ]==O00000OO000O0OOO0 :#line:545
        OOOOOO00O0OO0000O .namelist [OOOOOO00O0OO0000O .index ][0 ].setBackground ("hook_gold.png")#line:546
    elif OOOOOO00O0OO0000O .namelist [OOOOOO00O0OO0000O .index ][1 ]==O000OOO0OO000O00O :#line:547
        OOOOOO00O0OO0000O .namelist [OOOOOO00O0OO0000O .index ][0 ].setBackground ("hook_diamond.png")#line:548
    else :#line:549
        OOOOOO00O0OO0000O .namelist [OOOOOO00O0OO0000O .index ][0 ].setBackground ("hook_stone.png")#line:550
def getBorder ():#line:552
    return borderr #line:553
name="VipCode"