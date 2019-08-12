#coding:utf-8
#Python中声明文件编码的注释，编码格式指定为utf-8
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
from smbus import SMBus

XRservo = SMBus(1)

#######################################
#############信号引脚定义##############
#######################################
GPIO.setmode(GPIO.BCM)
#######################################
#########管脚类型设置及初始化##########
#######################################
GPIO.setwarnings(False)


########超声波接口定义#################
ECHO = 4	#超声波接收脚位
TRIG = 17	#超声波发射脚位

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4


#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

##########超声波模块管脚类型设置#########
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#超声波模块发射端管脚设置trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#超声波模块接收端管脚设置echo
XRservo.XiaoRGEEK_SetServo(0x07,70)	##设置1舵机角度90°
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)

	
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)

	
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)

def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)

def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
####################################################
##函数名称 ：Get_Distence()
##函数功能 超声波测距，返回距离（单位是米）
##入口参数 ：无
##出口参数 ：无
####################################################
def	Get_Distence():
	time.sleep(0.05)
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
				pass
	t1 = time.time()
	while GPIO.input(ECHO):
				pass
	t2 = time.time()
	time.sleep(0.1)
	dis=(t2-t1)*340/2*100
	print 'Distance: %d cm' %dis
	return dis
	
	
	
####################################################
##函数名称 Send_Distance()
##函数功能 ：超声波距离PC端显示
##入口参数 ：无
##出口参数 ：无
####################################################
def Wava_Avoiddance():
	dis=int(Get_Distence())
	time.sleep(0.05)
	if dis > 25:
		Motor_Forward()
	else :
		Motor_Backward
		time.sleep(0.3)
		Motor_Stop()
		XRservo.XiaoRGEEK_SetServo(0x07,10)	##设置1舵机角度90°
		time.sleep(1)
		distance_L=int(Get_Distence())
		time.sleep(1)
		XRservo.XiaoRGEEK_SetServo(0x07,65)	##设置1舵机角度90°
		time.sleep(1)
		distance_M=int(Get_Distence())
		time.sleep(1)
		XRservo.XiaoRGEEK_SetServo(0x07,130)	##
		time.sleep(1)
		distance_R=int(Get_Distence())
		time.sleep(1)
		if (distance_L<distance_R) & (distance_M<distance_R):
			Motor_TurnLeft()
			time.sleep(0.3)
			Motor_Stop()
		elif (distance_L<distance_M) & (distance_R<distance_M):
			Motor_Forward()
		elif (distance_M<distance_L) & (distance_R<distance_L):
			Motor_TurnRight()
			time.sleep(0.3)
			Motor_Stop()
		XRservo.XiaoRGEEK_SetServo(0x07,65)	##设置1舵机角度90°
		time.sleep(1)
		
			
'''
循环检测
'''
while True:
	Wava_Avoiddance()
	print 'ddddddd'